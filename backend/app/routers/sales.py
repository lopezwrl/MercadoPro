from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import or_, func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Customer, Sale, SaleItem, Product, StockMovement, Inventory, AuditLog, CashRegister, CashMovement, SalePayment
from app.routers.auth import get_current_user

router=APIRouter(tags=['Clientes e Vendas'])

def D(v): return Decimal(str(v or 0))

def audit(db,user,action,desc):
    db.add(AuditLog(username=user.username, action=action, description=desc))

class CustomerIn(BaseModel):
    code: str|None=None; name: str; trade_name: str|None=None; cpf: str|None=None; cnpj: str|None=None; rg: str|None=None
    phone: str|None=None; mobile: str|None=None; email: str|None=None; cep: str|None=None; street: str|None=None; number: str|None=None
    complement: str|None=None; neighborhood: str|None=None; city: str|None=None; state: str|None=None; notes: str|None=None
    birth_date: str|None=None; active: bool=True

class SaleItemIn(BaseModel):
    product_id:int; quantity:Decimal=Field(gt=0); discount:Decimal=Field(default=0,ge=0)
class PaymentIn(BaseModel):
    payment_type:str; amount:Decimal=Field(gt=0); received_amount:Decimal=Field(default=0,ge=0)
class SaleIn(BaseModel):
    customer_id:int|None=None; discount:Decimal=Field(default=0,ge=0); notes:str|None=None; items:list[SaleItemIn]=Field(min_length=1)

@router.get('/customers')
def customers(q:str='',status:str='',page:int=1,size:int=50,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    query=db.query(Customer)
    if q:
        like=f'%{q}%'; query=query.filter(or_(Customer.code.ilike(like),Customer.name.ilike(like),Customer.cpf.ilike(like),Customer.cnpj.ilike(like),Customer.phone.ilike(like),Customer.email.ilike(like)))
    if status: query=query.filter(Customer.active==(status=='ATIVO'))
    total=query.count(); rows=query.order_by(Customer.name).offset((page-1)*size).limit(size).all()
    return {'items':[customer_out(x) for x in rows],'total':total,'page':page,'pages':(total+size-1)//size}

def customer_out(x):
    return {'id':x.id,'code':x.code,'name':x.name,'trade_name':x.trade_name,'cpf':x.cpf,'cnpj':x.cnpj,'phone':x.phone,'mobile':x.mobile,'email':x.email,'cep':x.cep,'street':x.street,'number':x.number,'complement':x.complement,'neighborhood':x.neighborhood,'city':x.city,'state':x.state,'notes':x.notes,'birth_date':x.birth_date.isoformat() if x.birth_date else None,'active':x.active}

@router.post('/customers')
def create_customer(data:CustomerIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    if data.cpf and db.query(Customer).filter(Customer.cpf==data.cpf).first(): raise HTTPException(409,'CPF já cadastrado.')
    if data.cnpj and db.query(Customer).filter(Customer.cnpj==data.cnpj).first(): raise HTTPException(409,'CNPJ já cadastrado.')
    code=data.code or f'CLI-{int(datetime.utcnow().timestamp())}'
    if db.query(Customer).filter(Customer.code==code).first(): raise HTTPException(409,'Código de cliente já cadastrado.')
    payload=data.model_dump(); payload['code']=code
    if payload.get('birth_date'): payload['birth_date']=datetime.fromisoformat(payload['birth_date']).date()
    obj=Customer(**payload); db.add(obj); audit(db,user,'CLIENTE_CRIADO',f'Cliente {code} criado.'); db.commit(); db.refresh(obj); return customer_out(obj)

@router.patch('/customers/{customer_id}')
def update_customer(customer_id:int,data:CustomerIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    obj=db.get(Customer,customer_id)
    if not obj: raise HTTPException(404,'Cliente não encontrado.')
    if data.cpf and db.query(Customer).filter(Customer.cpf==data.cpf,Customer.id!=customer_id).first(): raise HTTPException(409,'CPF já cadastrado.')
    if data.cnpj and db.query(Customer).filter(Customer.cnpj==data.cnpj,Customer.id!=customer_id).first(): raise HTTPException(409,'CNPJ já cadastrado.')
    for k,v in data.model_dump().items():
        if k=='birth_date' and v: v=datetime.fromisoformat(v).date()
        setattr(obj,k,v)
    audit(db,user,'CLIENTE_ALTERADO',f'Cliente {obj.code} alterado.'); db.commit(); db.refresh(obj); return customer_out(obj)

@router.patch('/customers/{customer_id}/status')
def customer_status(customer_id:int,active:bool,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    obj=db.get(Customer,customer_id)
    if not obj: raise HTTPException(404,'Cliente não encontrado.')
    obj.active=active; audit(db,user,'CLIENTE_STATUS',f'Cliente {obj.code}: {"ativo" if active else "inativo"}.'); db.commit(); return customer_out(obj)

@router.get('/sales')
def sales(q:str='',status:str='',db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    query=db.query(Sale).order_by(Sale.created_at.desc())
    if q: query=query.filter(or_(Sale.number.ilike(f'%{q}%'),Sale.status.ilike(f'%{q}%')))
    if status: query=query.filter(Sale.status==status)
    rows=query.limit(200).all()
    return {'items':[sale_out(x) for x in rows],'total':query.count()}

def sale_out(x):
    return {'id':x.id,'number':x.number,'customer':x.customer.name if x.customer else 'Consumidor não identificado','customer_id':x.customer_id,'user':x.user.name if x.user else '', 'sale_date':x.sale_date.isoformat(),'status':x.status,'subtotal':float(x.subtotal),'discount':float(x.discount),'total':float(x.total),'items_count':len(x.items)}

@router.get('/sales/search')
def sales_search(q:str='',db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    return sales(q=q,db=db,user=user)

@router.get('/sales/{sale_id}')
def sale_detail(sale_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    x=db.get(Sale,sale_id)
    if not x: raise HTTPException(404,'Venda não encontrada.')
    return {**sale_out(x),'notes':x.notes,'payments':[{'id':p.id,'payment_type':p.payment_type,'amount':float(p.amount),'received_amount':float(p.received_amount),'change_amount':float(p.change_amount)} for p in db.query(SalePayment).filter(SalePayment.sale_id==x.id).all()],'items':[{'id':i.id,'product_id':i.product_id,'product':i.product.description,'quantity':float(i.quantity),'unit_price':float(i.unit_price),'discount':float(i.discount),'subtotal':float(i.subtotal)} for i in x.items]}

@router.post('/sales')
def create_sale(data:SaleIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    # Creates a pending sale; finalization is a separate transaction.
    if data.customer_id and not db.get(Customer,data.customer_id): raise HTTPException(404,'Cliente não encontrado.')
    number=f'VEN-{datetime.utcnow().strftime("%Y%m%d%H%M%S%f")}'
    sale=Sale(number=number,customer_id=data.customer_id,user_id=user.id,status='PENDENTE',discount=D(data.discount),notes=data.notes,subtotal=0,total=0)
    db.add(sale); db.flush()
    subtotal=Decimal('0')
    for row in data.items:
        p=db.get(Product,row.product_id)
        if not p or not p.active: db.rollback(); raise HTTPException(400,f'Produto {row.product_id} inexistente ou inativo.')
        qty=D(row.quantity); disc=D(row.discount); unit=D(p.sale_price); line=max(Decimal('0'),qty*unit-disc); subtotal+=qty*unit
        db.add(SaleItem(sale_id=sale.id,product_id=p.id,quantity=qty,unit_id=p.unit_id,unit_price=unit,discount=disc,subtotal=line))
    sale.subtotal=subtotal; sale.total=max(Decimal('0'),subtotal-D(data.discount)-sum((D(i.discount) for i in sale.items),Decimal('0'))); audit(db,user,'VENDA_CRIADA',f'Venda {number} criada em rascunho.'); db.commit(); db.refresh(sale); return sale_detail(sale.id,db,user)

@router.post('/sales/{sale_id}/items')
def add_sale_item(sale_id:int,data:SaleItemIn,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    sale=db.get(Sale,sale_id); p=db.get(Product,data.product_id)
    if not sale or sale.status!='PENDENTE': raise HTTPException(400,'Venda não está pendente.')
    if not p or not p.active: raise HTTPException(400,'Produto inexistente ou inativo.')
    item=SaleItem(sale_id=sale.id,product_id=p.id,quantity=D(data.quantity),unit_id=p.unit_id,unit_price=D(p.sale_price),discount=D(data.discount),subtotal=max(Decimal('0'),D(data.quantity)*D(p.sale_price)-D(data.discount)))
    db.add(item); db.flush(); sale.subtotal=sum((D(i.subtotal) for i in sale.items),Decimal('0')); sale.total=max(Decimal('0'),sale.subtotal-D(sale.discount)-sum((D(i.discount) for i in sale.items),Decimal('0'))); db.commit(); return sale_detail(sale.id,db,user)

@router.post('/sales/{sale_id}/finalize')
def finalize_sale(sale_id:int, data:list[PaymentIn]=[], db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    sale=db.get(Sale,sale_id)
    if not sale: raise HTTPException(404,'Venda não encontrada.')
    if sale.status!='PENDENTE': raise HTTPException(400,'A venda não está pendente.')
    if not sale.items: raise HTTPException(400,'A venda não possui itens.')
    try:
        cash=db.query(CashRegister).filter(CashRegister.status=='ABERTO').order_by(CashRegister.opened_at.desc()).first()
        if not cash: raise HTTPException(409,'Nenhum caixa está aberto. Abra o caixa antes de finalizar a venda.')
        allowed={'DINHEIRO','PIX','DEBITO','CREDITO'}
        if not data: raise HTTPException(400,'Informe ao menos uma forma de pagamento.')
        if any(p.payment_type.upper() not in allowed for p in data): raise HTTPException(400,'Forma de pagamento inválida.')
        paid=sum((D(p.amount) for p in data),Decimal('0'))
        if paid < D(sale.total): raise HTTPException(400,f'Pagamento insuficiente. Faltam R$ {D(sale.total)-paid:.2f}.')
        if paid > D(sale.total) and not any(p.payment_type.upper()=='DINHEIRO' for p in data): raise HTTPException(400,'Troco somente pode ser aplicado em dinheiro.')
        # lock rows where supported by PostgreSQL
        for item in sale.items:
            p=db.query(Product).filter(Product.id==item.product_id).with_for_update().first()
            if not p or not p.active: raise HTTPException(400,'Produto inválido.')
            if D(p.current_stock)<D(item.quantity): raise HTTPException(400,f'Estoque insuficiente para {p.description}. Disponível: {p.current_stock}.')
        for item in sale.items:
            p=db.query(Product).filter(Product.id==item.product_id).with_for_update().first(); prev=D(p.current_stock); new=prev-D(item.quantity); p.current_stock=new
            inv=db.query(Inventory).filter(Inventory.product_id==p.id).first()
            if inv: inv.quantity=new
            else: db.add(Inventory(product_id=p.id,quantity=new))
            db.add(StockMovement(product_id=p.id,quantity=D(item.quantity),movement_type='EXIT',user_id=user.id,reason=f'Venda {sale.number}',previous_stock=prev,resulting_stock=new))
        for pay in data:
            typ=pay.payment_type.upper(); amount=D(pay.amount); received=D(pay.received_amount) if typ=='DINHEIRO' else amount
            change=max(Decimal('0'),received-amount)
            db.add(SalePayment(sale_id=sale.id,payment_type=typ,amount=amount,received_amount=received,change_amount=change))
            if typ=='DINHEIRO':
                db.add(CashMovement(cash_register_id=cash.id,user_id=user.id,movement_type='VENDA',amount=amount,description=f'Venda {sale.number}',sale_id=sale.id))
        sale.status='FINALIZADA'; sale.sale_date=datetime.utcnow(); audit(db,user,'VENDA_FINALIZADA',f'Venda {sale.number} finalizada; estoque baixado e pagamento registrado.')
        db.commit(); db.refresh(sale); return sale_detail(sale.id,db,user)
    except HTTPException:
        db.rollback(); raise
    except Exception as e:
        db.rollback(); raise HTTPException(500,f'Falha transacional ao finalizar venda: {e}')

@router.post('/sales/{sale_id}/cancel')
def cancel_sale(sale_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    sale=db.get(Sale,sale_id)
    if not sale: raise HTTPException(404,'Venda não encontrada.')
    if user.role not in ('ADMINISTRADOR','GERENTE'): raise HTTPException(403,'Somente ADMINISTRADOR ou GERENTE podem cancelar vendas.')
    if sale.status=='CANCELADA': raise HTTPException(400,'Venda já cancelada.')
    if sale.status!='FINALIZADA': sale.status='CANCELADA'; audit(db,user,'VENDA_CANCELADA',f'Venda {sale.number} cancelada.'); db.commit(); return sale_detail(sale.id,db,user)
    try:
        cash=db.query(CashRegister).filter(CashRegister.status=='ABERTO').order_by(CashRegister.opened_at.desc()).first()
        payments=db.query(SalePayment).filter(SalePayment.sale_id==sale.id).all()
        if any(p.payment_type=='DINHEIRO' for p in payments) and not cash: raise HTTPException(409,'Abra o caixa para estornar uma venda paga em dinheiro.')
        for item in sale.items:
            p=db.query(Product).filter(Product.id==item.product_id).with_for_update().first(); prev=D(p.current_stock); new=prev+D(item.quantity); p.current_stock=new
            inv=db.query(Inventory).filter(Inventory.product_id==p.id).first()
            if inv: inv.quantity=new
            else: db.add(Inventory(product_id=p.id,quantity=new))
            db.add(StockMovement(product_id=p.id,quantity=D(item.quantity),movement_type='RETURN',user_id=user.id,reason=f'Estorno da venda {sale.number}',previous_stock=prev,resulting_stock=new))
        if cash:
            for p in payments:
                if p.payment_type=='DINHEIRO': db.add(CashMovement(cash_register_id=cash.id,user_id=user.id,movement_type='ESTORNO_VENDA',amount=-D(p.amount),description=f'Estorno da venda {sale.number}',sale_id=sale.id))
        sale.status='CANCELADA'; audit(db,user,'VENDA_CANCELADA',f'Venda {sale.number} cancelada e estoque estornado.'); db.commit(); db.refresh(sale); return sale_detail(sale.id,db,user)
    except Exception as e:
        db.rollback(); raise HTTPException(500,f'Falha transacional no cancelamento: {e}')
