from datetime import datetime
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from app.core.database import get_db
from app.models.models import Supplier, SupplierProduct, Purchase, PurchaseItem, Product, Inventory, StockMovement, User
from app.routers.auth import get_current_user

router = APIRouter(tags=["Fornecedores e Compras"])

class SupplierIn(BaseModel):
    code: str = Field(min_length=1, max_length=30)
    legal_name: str | None = None
    trade_name: str = Field(min_length=1, max_length=180)
    cnpj: str | None = None
    state_registration: str | None = None
    cpf: str | None = None
    phone: str | None = None
    mobile: str | None = None
    email: str | None = None
    cep: str | None = None
    street: str | None = None
    number: str | None = None
    complement: str | None = None
    neighborhood: str | None = None
    city: str | None = None
    state: str | None = None
    notes: str | None = None
    active: bool = True

class SupplierOut(SupplierIn):
    model_config = ConfigDict(from_attributes=True)
    id: int

class SupplierProductIn(BaseModel):
    supplier_id: int
    product_id: int
    supplier_product_code: str | None = None
    negotiated_cost: Decimal | None = Field(default=None, ge=0)
    delivery_days: int | None = Field(default=None, ge=0)
    notes: str | None = None
    active: bool = True

class PurchaseItemIn(BaseModel):
    product_id: int
    quantity: Decimal = Field(gt=0)
    unit_id: int
    unit_cost: Decimal = Field(ge=0)
    discount: Decimal = Field(default=Decimal("0"), ge=0)
    surcharge: Decimal = Field(default=Decimal("0"), ge=0)
    lot: str | None = None
    expiry_date: datetime | None = None

class PurchaseIn(BaseModel):
    number: str = Field(min_length=1, max_length=40)
    supplier_id: int
    purchase_date: datetime | None = None
    discount: Decimal = Field(default=Decimal("0"), ge=0)
    surcharge: Decimal = Field(default=Decimal("0"), ge=0)
    freight: Decimal = Field(default=Decimal("0"), ge=0)
    notes: str | None = None
    items: list[PurchaseItemIn] = Field(default_factory=list)


def supplier_dict(s: Supplier):
    return {c.name: getattr(s, c.name) for c in Supplier.__table__.columns}

@router.get("/suppliers", response_model=list[SupplierOut])
def list_suppliers(q: str = "", status: str = "", city: str = "", state: str = "", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Supplier)
    if q:
        like = f"%{q.strip()}%"
        query = query.filter(or_(Supplier.code.ilike(like), Supplier.trade_name.ilike(like), Supplier.legal_name.ilike(like), Supplier.cnpj.ilike(like)))
    if status == "active": query = query.filter(Supplier.active.is_(True))
    if status == "inactive": query = query.filter(Supplier.active.is_(False))
    if city: query = query.filter(Supplier.city.ilike(f"%{city}%"))
    if state: query = query.filter(Supplier.state == state.upper())
    return query.order_by(Supplier.trade_name).all()

@router.post("/suppliers", response_model=SupplierOut)
def create_supplier(data: SupplierIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if db.query(Supplier).filter(Supplier.code == data.code).first(): raise HTTPException(409, "Código do fornecedor já existe.")
    if data.cnpj and db.query(Supplier).filter(Supplier.cnpj == data.cnpj).first(): raise HTTPException(409, "CNPJ do fornecedor já existe.")
    s = Supplier(**data.model_dump())
    db.add(s); db.flush()
    db.add(__import__('app.models.models', fromlist=['AuditLog']).AuditLog(username=user.username, action="CREATE_SUPPLIER", description=f"Fornecedor {s.id} - {s.trade_name}"))
    db.commit(); db.refresh(s); return s

@router.patch("/suppliers/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, data: SupplierIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = db.get(Supplier, supplier_id)
    if not s: raise HTTPException(404, "Fornecedor não encontrado.")
    if db.query(Supplier).filter(Supplier.code == data.code, Supplier.id != supplier_id).first(): raise HTTPException(409, "Código do fornecedor já existe.")
    if data.cnpj and db.query(Supplier).filter(Supplier.cnpj == data.cnpj, Supplier.id != supplier_id).first(): raise HTTPException(409, "CNPJ do fornecedor já existe.")
    for k,v in data.model_dump().items(): setattr(s,k,v)
    db.add(__import__('app.models.models', fromlist=['AuditLog']).AuditLog(username=user.username, action="UPDATE_SUPPLIER", description=f"Fornecedor {s.id} - {s.trade_name}"))
    db.commit(); db.refresh(s); return s

@router.patch("/suppliers/{supplier_id}/status", response_model=SupplierOut)
def toggle_supplier(supplier_id: int, active: bool, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    s = db.get(Supplier, supplier_id)
    if not s: raise HTTPException(404, "Fornecedor não encontrado.")
    s.active = active
    db.add(__import__('app.models.models', fromlist=['AuditLog']).AuditLog(username=user.username, action="ACTIVATE_SUPPLIER" if active else "DEACTIVATE_SUPPLIER", description=f"Fornecedor {s.id}"))
    db.commit(); db.refresh(s); return s

@router.post("/supplier-products")
def save_supplier_product(data: SupplierProductIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.get(Supplier, data.supplier_id): raise HTTPException(404, "Fornecedor não encontrado.")
    if not db.get(Product, data.product_id): raise HTTPException(404, "Produto não encontrado.")
    row = db.query(SupplierProduct).filter(SupplierProduct.supplier_id==data.supplier_id, SupplierProduct.product_id==data.product_id).first()
    if row:
        for k,v in data.model_dump().items(): setattr(row,k,v)
    else:
        row = SupplierProduct(**data.model_dump()); db.add(row)
    db.commit(); db.refresh(row)
    return {c.name:getattr(row,c.name) for c in SupplierProduct.__table__.columns}


def purchase_total(p: Purchase, items):
    subtotal = sum((i.quantity*i.unit_cost for i in items), Decimal("0"))
    item_adjust = sum((i.surcharge-i.discount for i in items), Decimal("0"))
    p.subtotal = subtotal
    p.total = subtotal + item_adjust + p.surcharge + p.freight - p.discount
    if p.total < 0: raise HTTPException(400, "O total da compra não pode ser negativo.")
    return p.total


def purchase_out(p: Purchase):
    return {
        "id": p.id, "number": p.number, "supplier_id": p.supplier_id,
        "supplier": p.supplier.trade_name if p.supplier else None,
        "purchase_date": p.purchase_date, "user": p.user.name if p.user else None,
        "status": p.status, "subtotal": p.subtotal, "discount": p.discount,
        "surcharge": p.surcharge, "freight": p.freight, "total": p.total,
        "notes": p.notes,
        "items": [{"id":i.id,"product_id":i.product_id,"product":i.product.description if i.product else None,
                   "internal_code":i.product.internal_code if i.product else None,"quantity":i.quantity,"unit_id":i.unit_id,
                   "unit_cost":i.unit_cost,"discount":i.discount,"surcharge":i.surcharge,"total":i.total,
                   "lot":i.lot,"expiry_date":i.expiry_date} for i in p.items]
    }

@router.get("/purchases")
def list_purchases(q: str = "", supplier_id: int|None = None, status: str = "", date_from: datetime|None = None, date_to: datetime|None = None, page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Purchase).options(joinedload(Purchase.supplier), joinedload(Purchase.user), joinedload(Purchase.items).joinedload(PurchaseItem.product))
    if q: query = query.filter(Purchase.number.ilike(f"%{q}%"))
    if supplier_id: query = query.filter(Purchase.supplier_id == supplier_id)
    if status: query = query.filter(Purchase.status == status)
    if date_from: query = query.filter(Purchase.purchase_date >= date_from)
    if date_to: query = query.filter(Purchase.purchase_date <= date_to)
    total = query.count()
    rows = query.order_by(Purchase.purchase_date.desc()).offset((page-1)*page_size).limit(page_size).all()
    return {"items":[purchase_out(x) for x in rows],"total":total,"page":page,"page_size":page_size,"pages":(total+page_size-1)//page_size}

@router.post("/purchases")
def create_purchase(data: PurchaseIn, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not db.get(Supplier, data.supplier_id): raise HTTPException(404, "Fornecedor não encontrado.")
    if not db.query(Supplier).filter(Supplier.id==data.supplier_id, Supplier.active.is_(True)).first(): raise HTTPException(400, "O fornecedor está inativo.")
    if db.query(Purchase).filter(Purchase.number==data.number).first(): raise HTTPException(409, "Número da compra já existe.")
    if not data.items: raise HTTPException(400, "Adicione pelo menos um item à compra.")
    p = Purchase(number=data.number, supplier_id=data.supplier_id, purchase_date=data.purchase_date or datetime.utcnow(), user_id=user.id, discount=data.discount, surcharge=data.surcharge, freight=data.freight, notes=data.notes, status="RASCUNHO")
    db.add(p); db.flush()
    for x in data.items:
        product=db.get(Product,x.product_id)
        if not product or not product.active: raise HTTPException(400, f"Produto {x.product_id} não encontrado ou inativo.")
        item=PurchaseItem(purchase_id=p.id, **x.model_dump()); item.total=x.quantity*x.unit_cost+x.surcharge-x.discount
        p.items.append(item)
    purchase_total(p,p.items)
    from app.models.models import AuditLog
    db.add(AuditLog(username=user.username,action="CREATE_PURCHASE",description=f"Compra {p.number}"))
    db.commit(); db.refresh(p)
    p = db.query(Purchase).options(joinedload(Purchase.supplier),joinedload(Purchase.user),joinedload(Purchase.items).joinedload(PurchaseItem.product)).get(p.id)
    return purchase_out(p)

@router.get("/purchases/{purchase_id}")
def get_purchase(purchase_id:int, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    p=db.query(Purchase).options(joinedload(Purchase.supplier),joinedload(Purchase.user),joinedload(Purchase.items).joinedload(PurchaseItem.product)).get(purchase_id)
    if not p: raise HTTPException(404,"Compra não encontrada.")
    return purchase_out(p)

@router.patch("/purchases/{purchase_id}")
def update_purchase(purchase_id:int, data:PurchaseIn, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    p=db.query(Purchase).options(joinedload(Purchase.items)).get(purchase_id)
    if not p: raise HTTPException(404,"Compra não encontrada.")
    if p.status != "RASCUNHO": raise HTTPException(400,"Somente compras em rascunho podem ser editadas.")
    if p.number != data.number and db.query(Purchase).filter(Purchase.number==data.number,Purchase.id!=p.id).first(): raise HTTPException(409,"Número da compra já existe.")
    if not db.query(Supplier).filter(Supplier.id==data.supplier_id,Supplier.active.is_(True)).first(): raise HTTPException(400,"Fornecedor inválido ou inativo.")
    p.number=data.number; p.supplier_id=data.supplier_id; p.purchase_date=data.purchase_date or p.purchase_date; p.discount=data.discount; p.surcharge=data.surcharge; p.freight=data.freight; p.notes=data.notes
    p.items.clear()
    for x in data.items:
        product=db.get(Product,x.product_id)
        if not product or not product.active: raise HTTPException(400,f"Produto {x.product_id} não encontrado ou inativo.")
        item=PurchaseItem(**x.model_dump()); item.total=x.quantity*x.unit_cost+x.surcharge-x.discount; p.items.append(item)
    if not p.items: raise HTTPException(400,"Adicione pelo menos um item à compra.")
    purchase_total(p,p.items)
    from app.models.models import AuditLog
    db.add(AuditLog(username=user.username,action="UPDATE_PURCHASE",description=f"Compra {p.number}"))
    db.commit(); db.refresh(p)
    return get_purchase(p.id,db,user)

@router.post("/purchases/{purchase_id}/finalize")
def finalize_purchase(purchase_id:int, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    p=db.query(Purchase).options(joinedload(Purchase.items)).with_for_update().get(purchase_id)
    if not p: raise HTTPException(404,"Compra não encontrada.")
    if p.status != "RASCUNHO": raise HTTPException(400,"Apenas compras em rascunho podem ser finalizadas.")
    if not p.items: raise HTTPException(400,"Compra sem itens.")
    try:
        for item in p.items:
            product=db.query(Product).with_for_update().get(item.product_id)
            if not product or not product.active: raise HTTPException(400,f"Produto {item.product_id} inválido.")
            previous=Decimal(product.current_stock or 0); resulting=previous+Decimal(item.quantity)
            product.current_stock=resulting
            # Custo médio ponderado; evita alteração do preço de venda.
            old_cost=Decimal(product.cost_price or 0); qty_before=previous; qty_in=Decimal(item.quantity); new_cost=Decimal(item.unit_cost)
            if qty_before+qty_in > 0:
                product.cost_price=((old_cost*qty_before)+(new_cost*qty_in))/(qty_before+qty_in)
            db.add(StockMovement(product_id=product.id,quantity=item.quantity,movement_type="ENTRY",user_id=user.id,reason=f"Entrada de compra {p.number}",previous_stock=previous,resulting_stock=resulting))
        p.status="FINALIZADA"; purchase_total(p,p.items)
        from app.models.models import AuditLog
        db.add(AuditLog(username=user.username,action="FINALIZE_PURCHASE",description=f"Compra {p.number} finalizada e estoque atualizado"))
        db.commit()
    except HTTPException:
        db.rollback(); raise
    except Exception as e:
        db.rollback(); raise HTTPException(500,f"Não foi possível finalizar a compra: {e}")
    return get_purchase(purchase_id,db,user)

@router.post("/purchases/{purchase_id}/cancel")
def cancel_purchase(purchase_id:int, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    p=db.query(Purchase).options(joinedload(Purchase.items)).with_for_update().get(purchase_id)
    if not p: raise HTTPException(404,"Compra não encontrada.")
    if p.status == "CANCELADA": raise HTTPException(400,"A compra já está cancelada.")
    if p.status == "RASCUNHO":
        p.status="CANCELADA"
    else:
        try:
            for item in p.items:
                product=db.query(Product).with_for_update().get(item.product_id)
                previous=Decimal(product.current_stock or 0); qty=Decimal(item.quantity); resulting=previous-qty
                if resulting < 0: raise HTTPException(400,f"Não é possível estornar {product.description}: o estoque atual é insuficiente.")
                product.current_stock=resulting
                db.add(StockMovement(product_id=product.id,quantity=qty,movement_type="EXIT",user_id=user.id,reason=f"Estorno da compra {p.number}",previous_stock=previous,resulting_stock=resulting))
            p.status="CANCELADA"
        except HTTPException:
            db.rollback(); raise
        except Exception as e:
            db.rollback(); raise HTTPException(500,f"Não foi possível cancelar a compra: {e}")
    from app.models.models import AuditLog
    db.add(AuditLog(username=user.username,action="CANCEL_PURCHASE",description=f"Compra {p.number} cancelada"))
    db.commit()
    return get_purchase(purchase_id,db,user)
