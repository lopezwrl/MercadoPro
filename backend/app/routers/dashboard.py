from datetime import datetime, timedelta
from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, Product, Sale, SaleItem, CashRegister, CashMovement
from app.routers.auth import get_current_user
router=APIRouter(prefix="/dashboard",tags=["Dashboard"])
@router.get("/summary")
def summary(db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    products=db.query(Product).filter(Product.active==True).all(); today=datetime.utcnow(); near=today+timedelta(days=30); start=today.replace(hour=0,minute=0,second=0,microsecond=0); month=today.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
    sd=db.query(func.coalesce(func.sum(Sale.total),0),func.count(Sale.id)).filter(Sale.status=='FINALIZADA',Sale.sale_date>=start).first(); sm=db.query(func.coalesce(func.sum(Sale.total),0),func.count(Sale.id)).filter(Sale.status=='FINALIZADA',Sale.sale_date>=month).first()
    ps=db.query(func.coalesce(func.sum(SaleItem.quantity),0)).join(Sale).filter(Sale.status=='FINALIZADA',Sale.sale_date>=start).scalar() or 0
    cashreg=db.query(CashRegister).filter(CashRegister.status=="ABERTO").order_by(CashRegister.opened_at.desc()).first()
    cash_value=0
    if cashreg:
        cm=db.query(func.coalesce(func.sum(CashMovement.amount),0)).filter(CashMovement.cash_register_id==cashreg.id, CashMovement.movement_type!="ABERTURA").scalar() or 0
        cash_value=float(cashreg.opening_amount+cm)
    last=db.query(Sale).filter(Sale.status=='FINALIZADA').order_by(Sale.sale_date.desc()).limit(5).all()
    return {"sales_today":float(sd[0] or 0),"sales_month":float(sm[0] or 0),"sales_count":int(sd[1] or 0),"average_ticket":float((sd[0] or 0)/sd[1]) if sd[1] else 0,"products_sold":float(ps),"low_stock":sum(1 for p in products if p.current_stock>0 and p.current_stock<=p.min_stock),"near_expiry":sum(1 for p in products if p.expiry_date and p.expiry_date<=near),"out_of_stock":sum(1 for p in products if p.current_stock<=0),"total_products":len(products),"active_products":len(products),"payables":0,"receivables":0,"cash":cash_value,"estimated_profit":0,"demo":False,"latest_sales":[{"id":x.id,"number":x.number,"customer":x.customer.name if x.customer else "Consumidor não identificado","total":float(x.total),"sale_date":x.sale_date.isoformat()} for x in last]}
