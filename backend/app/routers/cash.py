from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, CashRegister, CashMovement, Sale, SalePayment
from app.routers.auth import get_current_user

router=APIRouter(prefix='/cash',tags=['Caixa'])

def D(v): return Decimal(str(v or 0))
def require_manager(user):
    if user.role not in ('ADMINISTRADOR','GERENTE'): raise HTTPException(403,'Somente ADMINISTRADOR ou GERENTE podem executar esta operação.')

def current(db): return db.query(CashRegister).filter(CashRegister.status=='ABERTO').order_by(CashRegister.opened_at.desc()).first()

class OpenIn(BaseModel): opening_amount: Decimal=Field(default=0,ge=0)
class MoveIn(BaseModel): movement_type:str; amount:Decimal=Field(gt=0); description:str=Field(min_length=2,max_length=250)
class CloseIn(BaseModel): closing_amount:Decimal=Field(ge=0)

@router.get('/status')
def status(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    r=current(db)
    if not r: return {'open':False,'register':None}
    cash_sales=db.query(func.coalesce(func.sum(SalePayment.amount),0)).join(Sale,Sale.id==SalePayment.sale_id).filter(SalePayment.payment_type=='DINHEIRO',Sale.status=='FINALIZADA',Sale.sale_date>=r.opened_at).scalar() or 0
    movements=db.query(func.coalesce(func.sum(CashMovement.amount),0)).filter(CashMovement.cash_register_id==r.id, CashMovement.movement_type!='ABERTURA').scalar() or 0
    expected=D(r.opening_amount)+D(movements)
    return {'open':True,'register':{'id':r.id,'opened_at':r.opened_at.isoformat(),'opening_amount':float(r.opening_amount),'expected_amount':float(expected),'cash_sales':float(cash_sales)}}

@router.post('/open')
def open_cash(data:OpenIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    require_manager(user)
    if current(db): raise HTTPException(409,'Já existe um caixa aberto.')
    r=CashRegister(opened_by=user.id,opening_amount=D(data.opening_amount),status='ABERTO')
    db.add(r); db.flush()
    if D(data.opening_amount): db.add(CashMovement(cash_register_id=r.id,user_id=user.id,movement_type='ABERTURA',amount=D(data.opening_amount),description='Saldo inicial do caixa'))
    db.commit(); db.refresh(r); return {'id':r.id,'status':r.status,'opening_amount':float(r.opening_amount)}

@router.post('/movement')
def movement(data:MoveIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    require_manager(user); r=current(db)
    if not r: raise HTTPException(409,'Abra o caixa antes de registrar movimentos.')
    typ=data.movement_type.upper()
    if typ not in ('SANGRIA','SUPRIMENTO'): raise HTTPException(400,'Tipo de movimento inválido.')
    amount=D(data.amount) if typ=='SUPRIMENTO' else -D(data.amount)
    db.add(CashMovement(cash_register_id=r.id,user_id=user.id,movement_type=typ,amount=amount,description=data.description))
    db.commit(); return status(db,user)

@router.post('/close')
def close_cash(data:CloseIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    require_manager(user); r=current(db)
    if not r: raise HTTPException(409,'Não existe caixa aberto.')
    movements=db.query(func.coalesce(func.sum(CashMovement.amount),0)).filter(CashMovement.cash_register_id==r.id, CashMovement.movement_type!='ABERTURA').scalar() or 0
    expected=D(r.opening_amount)+D(movements)
    # Payment rows are represented by movements when sales are finalized; expected is therefore authoritative.
    difference=D(data.closing_amount)-expected
    r.closed_by=user.id; r.closed_at=datetime.utcnow(); r.closing_amount=D(data.closing_amount); r.expected_amount=expected; r.difference=difference; r.status='FECHADO'
    db.commit(); return {'id':r.id,'status':'FECHADO','expected_amount':float(expected),'closing_amount':float(data.closing_amount),'difference':float(difference),'closed_at':r.closed_at.isoformat()}

@router.get('/history')
def history(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    rows=db.query(CashRegister).order_by(CashRegister.opened_at.desc()).limit(50).all()
    return {'items':[{'id':r.id,'opened_at':r.opened_at.isoformat(),'closed_at':r.closed_at.isoformat() if r.closed_at else None,'opening_amount':float(r.opening_amount),'expected_amount':float(r.expected_amount or 0),'closing_amount':float(r.closing_amount or 0),'difference':float(r.difference or 0),'status':r.status} for r in rows]}
