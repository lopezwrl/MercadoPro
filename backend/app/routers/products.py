from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.models import Product, Category, Subcategory, Brand, Unit, AuditLog
from app.routers.auth import get_current_user

router=APIRouter(prefix="/products",tags=["Produtos"])

def write_guard(user):
    if user.role not in {"ADMINISTRADOR","GERENTE","ESTOQUE"}: raise HTTPException(403,"Seu perfil não pode alterar produtos.")

def calculate_margin(cost, sale):
    cost=Decimal(cost or 0); sale=Decimal(sale or 0)
    return Decimal("0") if cost<=0 else ((sale-cost)/cost*100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def data(p):
    return {"id":p.id,"internal_code":p.internal_code,"barcode":p.barcode,"description":p.description,"short_description":p.short_description,"category_id":p.category_id,"subcategory_id":p.subcategory_id,"brand_id":p.brand_id,"unit_id":p.unit_id,"cost_price":float(p.cost_price or 0),"sale_price":float(p.sale_price or 0),"margin":float(p.margin or 0),"current_stock":float(p.current_stock or 0),"min_stock":float(p.min_stock or 0),"max_stock":float(p.max_stock or 0),"supplier_name":p.supplier_name,"location":p.location,"expiry_date":p.expiry_date,"active":p.active,"category":p.category.name if p.category else None,"brand":p.brand.name if p.brand else None,"unit":p.unit.code if p.unit else None}

@router.get("")
def list_products(q:str="",category_id:int|None=None,brand_id:int|None=None,active:bool|None=None,stock_status:str|None=None,page:int=Query(1,ge=1),limit:int=Query(20,ge=1,le=100),db:Session=Depends(get_db),user=Depends(get_current_user)):
    query=db.query(Product)
    if q: query=query.filter(or_(Product.description.ilike(f"%{q}%"),Product.internal_code.ilike(f"%{q}%"),Product.barcode.ilike(f"%{q}%")))
    if category_id: query=query.filter(Product.category_id==category_id)
    if brand_id: query=query.filter(Product.brand_id==brand_id)
    if active is not None: query=query.filter(Product.active==active)
    if stock_status=="out": query=query.filter(Product.current_stock<=0)
    elif stock_status=="low": query=query.filter(Product.current_stock>0,Product.current_stock<=Product.min_stock)
    elif stock_status=="normal": query=query.filter(Product.current_stock>Product.min_stock)
    total=query.count(); items=query.order_by(Product.description).offset((page-1)*limit).limit(limit).all()
    return {"items":[data(x) for x in items],"total":total,"page":page,"limit":limit,"pages":(total+limit-1)//limit}

@router.get("/{product_id}")
def get_product(product_id:int,db:Session=Depends(get_db),user=Depends(get_current_user)):
    p=db.get(Product,product_id)
    if not p: raise HTTPException(404,"Produto não encontrado.")
    return data(p)

@router.post("")
def create_product(payload:dict,db:Session=Depends(get_db),user=Depends(get_current_user)):
    write_guard(user)
    required=["internal_code","description","category_id","unit_id"]
    if any(not payload.get(x) for x in required): raise HTTPException(400,"Código, descrição, categoria e unidade são obrigatórios.")
    if db.query(Product).filter(Product.internal_code==payload["internal_code"]).first(): raise HTTPException(409,"Código interno já cadastrado.")
    barcode=payload.get("barcode") or None
    if barcode and db.query(Product).filter(Product.barcode==barcode).first(): raise HTTPException(409,"Código de barras já cadastrado.")
    category=db.get(Category,payload["category_id"]); unit=db.get(Unit,payload["unit_id"])
    if not category or not unit: raise HTTPException(400,"Categoria ou unidade inválida.")
    if payload.get("subcategory_id") and not db.get(Subcategory,payload["subcategory_id"]): raise HTTPException(400,"Subcategoria inválida.")
    cost=Decimal(str(payload.get("cost_price",0))); sale=Decimal(str(payload.get("sale_price",0)))
    if cost<0 or sale<0: raise HTTPException(400,"Preços não podem ser negativos.")
    min_s=Decimal(str(payload.get("min_stock",0))); max_s=Decimal(str(payload.get("max_stock",0)))
    if min_s<0 or max_s<0 or (max_s and min_s>max_s): raise HTTPException(400,"Estoque mínimo/máximo inválido.")
    p=Product(**{k:payload.get(k) for k in ["internal_code","barcode","description","short_description","category_id","subcategory_id","brand_id","unit_id","supplier_name","location"]},cost_price=cost,sale_price=sale,margin=calculate_margin(cost,sale),current_stock=Decimal(str(payload.get("current_stock",0))),min_stock=min_s,max_stock=max_s,expiry_date=payload.get("expiry_date"),active=payload.get("active",True))
    db.add(p); db.flush(); db.add(AuditLog(username=user.username,action="PRODUCT_CREATE",description=f"Produto {p.internal_code} criado.")); db.commit(); db.refresh(p); return data(p)

@router.patch("/{product_id}")
def update_product(product_id:int,payload:dict,db:Session=Depends(get_db),user=Depends(get_current_user)):
    write_guard(user); p=db.get(Product,product_id)
    if not p: raise HTTPException(404,"Produto não encontrado.")
    if "internal_code" in payload and payload["internal_code"]!=p.internal_code and db.query(Product).filter(Product.internal_code==payload["internal_code"]).first(): raise HTTPException(409,"Código interno já cadastrado.")
    if "barcode" in payload and payload["barcode"] and payload["barcode"]!=p.barcode and db.query(Product).filter(Product.barcode==payload["barcode"]).first(): raise HTTPException(409,"Código de barras já cadastrado.")
    for k in ["internal_code","barcode","description","short_description","category_id","subcategory_id","brand_id","unit_id","supplier_name","location","expiry_date","active"]:
        if k in payload: setattr(p,k,payload[k])
    if "cost_price" in payload: p.cost_price=Decimal(str(payload["cost_price"]))
    if "sale_price" in payload: p.sale_price=Decimal(str(payload["sale_price"]))
    if "min_stock" in payload: p.min_stock=Decimal(str(payload["min_stock"]))
    if "max_stock" in payload: p.max_stock=Decimal(str(payload["max_stock"]))
    if p.cost_price<0 or p.sale_price<0 or p.min_stock<0 or p.max_stock<0 or (p.max_stock and p.min_stock>p.max_stock): raise HTTPException(400,"Valores de preço/estoque inválidos.")
    p.margin=calculate_margin(p.cost_price,p.sale_price)
    db.add(AuditLog(username=user.username,action="PRODUCT_UPDATE",description=f"Produto {p.internal_code} alterado.")); db.commit(); db.refresh(p); return data(p)
