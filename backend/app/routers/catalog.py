from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.models import Category, Subcategory, Brand, Unit
from app.routers.auth import get_current_user

router = APIRouter(tags=["Cadastros"])

def guard(user, write=False):
    if user.role not in {"ADMINISTRADOR", "GERENTE", "ESTOQUE"} and write:
        raise HTTPException(403, "Seu perfil não possui permissão para alterar cadastros.")

def crud_router(model, path, label):
    r = APIRouter(prefix=path, tags=[label])
    @r.get("")
    def list_items(q: str = "", active: bool | None = None, db: Session = Depends(get_db), user=Depends(get_current_user)):
        query = db.query(model)
        if q: query = query.filter(model.name.ilike(f"%{q}%"))
        if active is not None: query = query.filter(model.active == active)
        return query.order_by(model.name).all()
    @r.post("")
    def create_item(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
        guard(user, True)
        name = (payload.get("name") or "").strip()
        if not name: raise HTTPException(400, "Nome é obrigatório.")
        if db.query(model).filter(model.name == name).first(): raise HTTPException(409, "Já existe um cadastro com esse nome.")
        obj = model(name=name)
        db.add(obj); db.commit(); db.refresh(obj); return obj
    @r.patch("/{item_id}")
    def update_item(item_id: int, payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
        guard(user, True); obj = db.get(model, item_id)
        if not obj: raise HTTPException(404, "Cadastro não encontrado.")
        if "name" in payload:
            name = (payload["name"] or "").strip()
            if not name: raise HTTPException(400, "Nome é obrigatório.")
            obj.name = name
        if "active" in payload: obj.active = bool(payload["active"])
        db.commit(); db.refresh(obj); return obj
    return r

categories = crud_router(Category, "/api/categories", "Categorias")
brands = crud_router(Brand, "/api/brands", "Marcas")

@categories.post("/subcategories")
def create_subcategory(payload: dict, db: Session = Depends(get_db), user=Depends(get_current_user)):
    guard(user, True); name=(payload.get("name") or "").strip(); category_id=payload.get("category_id")
    if not name or not category_id: raise HTTPException(400, "Categoria e nome são obrigatórios.")
    if not db.get(Category, category_id): raise HTTPException(404, "Categoria não encontrada.")
    if db.query(Subcategory).filter(Subcategory.category_id==category_id, Subcategory.name==name).first(): raise HTTPException(409, "Subcategoria já existe nessa categoria.")
    obj=Subcategory(name=name, category_id=category_id); db.add(obj); db.commit(); db.refresh(obj); return obj

@categories.get("/subcategories")
def list_subcategories(category_id: int|None=None, q: str="", db: Session=Depends(get_db), user=Depends(get_current_user)):
    query=db.query(Subcategory)
    if category_id: query=query.filter(Subcategory.category_id==category_id)
    if q: query=query.filter(Subcategory.name.ilike(f"%{q}%"))
    return query.order_by(Subcategory.name).all()

@categories.patch("/subcategories/{item_id}")
def update_subcategory(item_id:int,payload:dict,db:Session=Depends(get_db),user=Depends(get_current_user)):
    guard(user,True); obj=db.get(Subcategory,item_id)
    if not obj: raise HTTPException(404,"Subcategoria não encontrada.")
    if "name" in payload: obj.name=(payload["name"] or "").strip()
    if "category_id" in payload:
        if not db.get(Category,payload["category_id"]): raise HTTPException(404,"Categoria não encontrada.")
        obj.category_id=payload["category_id"]
    if "active" in payload: obj.active=bool(payload["active"])
    db.commit(); db.refresh(obj); return obj

@categories.get("/units")
def list_units(db:Session=Depends(get_db), user=Depends(get_current_user)): return db.query(Unit).order_by(Unit.code).all()
@categories.post("/units")
def create_unit(payload:dict,db:Session=Depends(get_db),user=Depends(get_current_user)):
    guard(user,True); code=(payload.get("code") or "").strip().upper(); name=(payload.get("name") or "").strip()
    if not code or not name: raise HTTPException(400,"Código e nome são obrigatórios.")
    if db.query(Unit).filter(Unit.code==code).first(): raise HTTPException(409,"Unidade já cadastrada.")
    obj=Unit(code=code,name=name); db.add(obj); db.commit(); db.refresh(obj); return obj
