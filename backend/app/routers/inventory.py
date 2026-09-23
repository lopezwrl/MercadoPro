from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import Product, StockMovement, AuditLog
from app.routers.auth import get_current_user

router=APIRouter(prefix="/inventory",tags=["Estoque"])

@router.get("/summary")
def summary(db:Session=Depends(get_db),user=Depends(get_current_user)):
    products=db.query(Product).filter(Product.active==True).all()
    return {"total_products":len(products),"active_products":len(products),"out_of_stock":sum(1 for p in products if p.current_stock<=0),"low_stock":sum(1 for p in products if p.current_stock>0 and p.current_stock<=p.min_stock),"near_expiry":sum(1 for p in products if p.expiry_date is not None)}

@router.post("/movements")
def movement(payload:dict,db:Session=Depends(get_db),user=Depends(get_current_user)):
    if user.role not in {"ADMINISTRADOR","GERENTE","ESTOQUE"}: raise HTTPException(403,"Seu perfil não pode movimentar estoque.")
    product=db.get(Product,payload.get("product_id")); mtype=payload.get("movement_type"); qty=Decimal(str(payload.get("quantity",0)))
    if not product: raise HTTPException(404,"Produto não encontrado.")
    if mtype not in {"ENTRY","EXIT","ADJUSTMENT","LOSS","RETURN"}: raise HTTPException(400,"Tipo de movimentação inválido.")
    if qty<=0: raise HTTPException(400,"A quantidade deve ser maior que zero.")
    previous=Decimal(product.current_stock or 0)
    if mtype in {"ENTRY","RETURN"}: resulting=previous+qty
    elif mtype in {"EXIT","LOSS"}: resulting=previous-qty
    else: resulting=qty
    if resulting<0: raise HTTPException(400,"Operação não permitida: estoque não pode ficar negativo.")
    product.current_stock=resulting
    obj=StockMovement(product_id=product.id,quantity=qty,movement_type=mtype,user_id=user.id,reason=payload.get("reason"),previous_stock=previous,resulting_stock=resulting)
    db.add(obj); db.add(AuditLog(username=user.username,action="STOCK_MOVEMENT",description=f"{mtype} de {qty} no produto {product.internal_code}."))
    db.commit(); db.refresh(obj)
    return {"id":obj.id,"product_id":product.id,"movement_type":mtype,"quantity":float(qty),"previous_stock":float(previous),"resulting_stock":float(resulting)}

@router.get("/movements")
def movements(product_id:int|None=None,movement_type:str|None=None,page:int=Query(1,ge=1),limit:int=Query(30,ge=1,le=100),db:Session=Depends(get_db),user=Depends(get_current_user)):
    query=db.query(StockMovement)
    if product_id: query=query.filter(StockMovement.product_id==product_id)
    if movement_type: query=query.filter(StockMovement.movement_type==movement_type)
    total=query.count(); rows=query.order_by(StockMovement.created_at.desc()).offset((page-1)*limit).limit(limit).all()
    return {"items":[{"id":x.id,"product_id":x.product_id,"product":x.product.description if x.product else "","movement_type":x.movement_type,"quantity":float(x.quantity),"previous_stock":float(x.previous_stock),"resulting_stock":float(x.resulting_stock),"reason":x.reason,"user":x.user.name if x.user else "","created_at":x.created_at} for x in rows],"total":total,"pages":(total+limit-1)//limit}
