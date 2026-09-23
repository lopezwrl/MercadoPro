from datetime import datetime, timedelta
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, desc
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Sale, SaleItem, Product, Purchase, PurchaseItem, StockMovement, FinancialEntry, SalePayment
from app.routers.auth import get_current_user

router=APIRouter(prefix='/reports',tags=['Reports'])

def dt(v):
    if not v: return None
    return datetime.fromisoformat(v)

def scope_dates(start,end):
    now=datetime.utcnow(); s=dt(start) if start else now.replace(hour=0,minute=0,second=0,microsecond=0)-timedelta(days=29); e=dt(end) if end else now
    return s,e

@router.get('/sales')
def sales_report(start:str|None=None,end:str|None=None,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    s,e=scope_dates(start,end)
    base=db.query(Sale).filter(Sale.status=='FINALIZADA',Sale.sale_date>=s,Sale.sale_date<=e)
    total=base.with_entities(func.coalesce(func.sum(Sale.total),0)).scalar() or 0
    count=base.with_entities(func.count(Sale.id)).scalar() or 0
    discount=base.with_entities(func.coalesce(func.sum(Sale.discount),0)).scalar() or 0
    daily=db.query(func.date(Sale.sale_date).label('day'),func.coalesce(func.sum(Sale.total),0).label('total'),func.count(Sale.id).label('count')).filter(Sale.status=='FINALIZADA',Sale.sale_date>=s,Sale.sale_date<=e).group_by(func.date(Sale.sale_date)).order_by(func.date(Sale.sale_date)).all()
    payments=db.query(SalePayment.payment_type,func.coalesce(func.sum(SalePayment.amount),0),func.count(SalePayment.id)).join(Sale,Sale.id==SalePayment.sale_id).filter(Sale.status=='FINALIZADA',Sale.sale_date>=s,Sale.sale_date<=e).group_by(SalePayment.payment_type).order_by(desc(func.sum(SalePayment.amount))).all()
    return {'period':{'start':s.isoformat(),'end':e.isoformat()},'summary':{'total':float(total),'count':count,'average_ticket':float(total/count) if count else 0,'discount':float(discount)},'daily':[{'date':str(x.day),'total':float(x.total),'count':x.count} for x in daily],'payments':[{'type':x[0],'total':float(x[1]),'count':x[2]} for x in payments]}

@router.get('/products')
def product_report(start:str|None=None,end:str|None=None,limit:int=10,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    s,e=scope_dates(start,end); limit=max(1,min(limit,50))
    rows=db.query(Product.id,Product.internal_code,Product.description,func.coalesce(func.sum(SaleItem.quantity),0).label('qty'),func.coalesce(func.sum(SaleItem.subtotal),0).label('revenue')).join(SaleItem,SaleItem.product_id==Product.id).join(Sale,Sale.id==SaleItem.sale_id).filter(Sale.status=='FINALIZADA',Sale.sale_date>=s,Sale.sale_date<=e).group_by(Product.id,Product.internal_code,Product.description).order_by(desc(func.sum(SaleItem.subtotal))).limit(limit).all()
    return {'items':[{'product_id':x.id,'code':x.internal_code,'description':x.description,'quantity':float(x.qty),'revenue':float(x.revenue)} for x in rows]}

@router.get('/stock')
def stock_report(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    products=db.query(Product).filter(Product.active==True).order_by(Product.description).all()
    total_cost=sum((Decimal(str(p.current_stock))*Decimal(str(p.cost_price)) for p in products),Decimal('0'))
    total_sale=sum((Decimal(str(p.current_stock))*Decimal(str(p.sale_price)) for p in products),Decimal('0'))
    low=[p for p in products if p.current_stock>0 and p.current_stock<=p.min_stock]
    zero=[p for p in products if p.current_stock<=0]
    return {'summary':{'products':len(products),'stock_cost':float(total_cost),'stock_sale':float(total_sale),'potential_margin':float(total_sale-total_cost),'low_stock':len(low),'out_of_stock':len(zero)},'items':[{'code':p.internal_code,'description':p.description,'stock':float(p.current_stock),'min_stock':float(p.min_stock),'cost':float(p.cost_price),'sale_price':float(p.sale_price),'stock_value':float(Decimal(str(p.current_stock))*Decimal(str(p.cost_price))),'status':'SEM ESTOQUE' if p.current_stock<=0 else 'BAIXO' if p.current_stock<=p.min_stock else 'NORMAL'} for p in products]}

@router.get('/finance')
def finance_report(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    pending=db.query(FinancialEntry).filter(FinancialEntry.status=='PENDENTE').all(); paid=db.query(FinancialEntry).filter(FinancialEntry.status=='PAGO').all()
    def sums(rows,typ): return float(sum((Decimal(str(x.amount)) for x in rows if x.entry_type==typ),Decimal('0')))
    today=datetime.utcnow().date(); overdue=[x for x in pending if x.due_date<today]
    return {'summary':{'pending_payables':sums(pending,'PAGAR'),'pending_receivables':sums(pending,'RECEBER'),'paid_payables':sums(paid,'PAGAR'),'received':sums(paid,'RECEBER'),'overdue_payables':sums(overdue,'PAGAR'),'overdue_receivables':sums(overdue,'RECEBER')},'overdue':[{'id':x.id,'type':x.entry_type,'description':x.description,'amount':float(x.amount),'due_date':x.due_date.isoformat(),'person':x.person} for x in overdue]}

@router.get('/purchases')
def purchases_report(start:str|None=None,end:str|None=None,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    s,e=scope_dates(start,end); rows=db.query(Purchase).filter(Purchase.status=='FINALIZADA',Purchase.purchase_date>=s,Purchase.purchase_date<=e).order_by(desc(Purchase.purchase_date)).all(); total=sum((Decimal(str(x.total)) for x in rows),Decimal('0'))
    suppliers={}
    for x in rows:
        name=x.supplier.trade_name if x.supplier else '—'; suppliers[name]=suppliers.get(name,0)+float(x.total)
    return {'summary':{'count':len(rows),'total':float(total),'average':float(total/len(rows)) if rows else 0},'by_supplier':[{'supplier':k,'total':v} for k,v in sorted(suppliers.items(),key=lambda z:z[1],reverse=True)],'items':[{'number':x.number,'date':x.purchase_date.isoformat(),'supplier':x.supplier.trade_name if x.supplier else '—','total':float(x.total)} for x in rows]}
