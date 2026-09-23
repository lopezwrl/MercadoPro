from datetime import datetime, date
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, AuditLog, Sale, Purchase, FinancialEntry, FinancialCategory
from app.routers.auth import get_current_user

router=APIRouter(prefix='/finance', tags=['Financeiro'])
def D(v): return Decimal(str(v or 0))
def audit(db,user,action,description): db.add(AuditLog(username=user.username,action=action,description=description))
def allowed(user):
    if user.role not in ('ADMINISTRADOR','GERENTE','FINANCEIRO'): raise HTTPException(403,'Sem permissão para esta operação.')
class EntryIn(BaseModel):
    entry_type:str; description:str=Field(min_length=2,max_length=250); amount:Decimal=Field(gt=0); due_date:date; category:str=Field(min_length=1,max_length=100); person:str|None=None; reference:str|None=None; notes:str|None=None
class CategoryIn(BaseModel): name:str=Field(min_length=2,max_length=100); entry_type:str

def serialize(e): return {'id':e.id,'entry_type':e.entry_type,'description':e.description,'amount':float(e.amount),'due_date':e.due_date.isoformat(),'category':e.category,'person':e.person,'reference':e.reference,'notes':e.notes,'status':e.status,'paid_at':e.paid_at.isoformat() if e.paid_at else None,'created_at':e.created_at.isoformat()}

@router.get('/summary')
def summary(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    today=date.today(); first=today.replace(day=1)
    sales_month=db.query(func.coalesce(func.sum(Sale.total),0)).filter(Sale.status=='FINALIZADA',func.date(Sale.sale_date)>=first).scalar() or 0
    purchases_month=db.query(func.coalesce(func.sum(Purchase.total),0)).filter(Purchase.status=='FINALIZADA',func.date(Purchase.purchase_date)>=first).scalar() or 0
    pay=db.query(func.coalesce(func.sum(FinancialEntry.amount),0)).filter(FinancialEntry.entry_type=='PAGAR',FinancialEntry.status=='PENDENTE').scalar() or 0
    rec=db.query(func.coalesce(func.sum(FinancialEntry.amount),0)).filter(FinancialEntry.entry_type=='RECEBER',FinancialEntry.status=='PENDENTE').scalar() or 0
    op=db.query(func.coalesce(func.sum(FinancialEntry.amount),0)).filter(FinancialEntry.entry_type=='PAGAR',FinancialEntry.status=='PENDENTE',FinancialEntry.due_date<today).scalar() or 0
    orc=db.query(func.coalesce(func.sum(FinancialEntry.amount),0)).filter(FinancialEntry.entry_type=='RECEBER',FinancialEntry.status=='PENDENTE',FinancialEntry.due_date<today).scalar() or 0
    return {'sales_month':float(sales_month),'purchases_month':float(purchases_month),'pending_payables':float(pay),'pending_receivables':float(rec),'overdue_payables':float(op),'overdue_receivables':float(orc),'balance_projection':float(D(sales_month)-D(purchases_month)-D(pay)+D(rec))}

@router.get('/categories')
def categories(entry_type:str|None=None,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    q=db.query(FinancialCategory).filter(FinancialCategory.active==True)
    if entry_type:q=q.filter(FinancialCategory.entry_type==entry_type.upper())
    return [{'id':x.id,'name':x.name,'entry_type':x.entry_type} for x in q.order_by(FinancialCategory.name).all()]

@router.post('/categories')
def create_category(data:CategoryIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    allowed(user); typ=data.entry_type.upper()
    if typ not in ('PAGAR','RECEBER'): raise HTTPException(400,'Tipo inválido.')
    if db.query(FinancialCategory).filter(FinancialCategory.name==data.name,FinancialCategory.entry_type==typ).first(): raise HTTPException(409,'Categoria já existe.')
    c=FinancialCategory(name=data.name,entry_type=typ); db.add(c); audit(db,user,'FINANCEIRO_CATEGORIA','Categoria criada: '+data.name); db.commit(); db.refresh(c); return {'id':c.id,'name':c.name,'entry_type':c.entry_type}

@router.get('/entries')
def entries(entry_type:str|None=None,status:str|None=None,q:str='',db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    query=db.query(FinancialEntry)
    if entry_type: query=query.filter(FinancialEntry.entry_type==entry_type.upper())
    if status: query=query.filter(FinancialEntry.status==status.upper())
    if q: query=query.filter(or_(FinancialEntry.description.ilike(f'%{q}%'),FinancialEntry.person.ilike(f'%{q}%'),FinancialEntry.reference.ilike(f'%{q}%')))
    rows=query.order_by(FinancialEntry.due_date.asc(),FinancialEntry.id.desc()).limit(200).all()
    return {'items':[serialize(x) for x in rows]}

@router.post('/entries')
def create_entry(data:EntryIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    allowed(user); typ=data.entry_type.upper()
    if typ not in ('PAGAR','RECEBER'): raise HTTPException(400,'Tipo inválido. Use PAGAR ou RECEBER.')
    if data.due_date < date(2000,1,1): raise HTTPException(400,'Data de vencimento inválida.')
    e=FinancialEntry(entry_type=typ,description=data.description,amount=D(data.amount),due_date=data.due_date,category=data.category,person=data.person,reference=data.reference,notes=data.notes,created_by=user.id)
    db.add(e); audit(db,user,'FINANCEIRO_LANCAMENTO',f'{typ}: {data.description} - R$ {D(data.amount):.2f}'); db.commit(); db.refresh(e); return serialize(e)

@router.post('/entries/{entry_id}/pay')
def pay_entry(entry_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    allowed(user); e=db.get(FinancialEntry,entry_id)
    if not e: raise HTTPException(404,'Lançamento não encontrado.')
    if e.status=='PAGO': raise HTTPException(400,'Lançamento já baixado.')
    e.status='PAGO'; e.paid_at=datetime.utcnow(); audit(db,user,'FINANCEIRO_BAIXA',f'Lançamento {e.id} baixado: {e.description}.'); db.commit(); db.refresh(e); return serialize(e)

@router.post('/entries/{entry_id}/cancel')
def cancel_entry(entry_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    allowed(user); e=db.get(FinancialEntry,entry_id)
    if not e: raise HTTPException(404,'Lançamento não encontrado.')
    if e.status=='PAGO': raise HTTPException(400,'Não cancele um lançamento já pago; faça um estorno em processo específico.')
    e.status='CANCELADO'; audit(db,user,'FINANCEIRO_CANCELAMENTO',f'Lançamento {e.id} cancelado.'); db.commit(); return serialize(e)

@router.get('/cash-flow')
def cash_flow(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    rows=db.query(FinancialEntry).order_by(FinancialEntry.due_date).limit(500).all()
    result={}
    for e in rows:
        key=e.due_date.isoformat(); result.setdefault(key,{'date':key,'payables':0,'receivables':0})
        if e.entry_type=='PAGAR': result[key]['payables']+=float(e.amount)
        else: result[key]['receivables']+=float(e.amount)
    return {'items':list(result.values())}
