from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import or_, desc
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.models import User, Permission, AuditLog, Setting
from app.routers.auth import get_current_user

router = APIRouter(prefix="/security", tags=["Segurança"])

ROLES = ["ADMINISTRADOR", "GERENTE", "CAIXA", "ESTOQUE", "FINANCEIRO"]
MODULES = ["DASHBOARD", "PDV", "CAIXA", "CLIENTES", "VENDAS", "FINANCEIRO", "RELATORIOS", "PRODUTOS", "ESTOQUE", "FORNECEDORES", "COMPRAS", "CADASTROS", "SEGURANCA"]

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=6, max_length=100)
    role: str = "CAIXA"
    active: bool = True

class UserUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    active: bool | None = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(min_length=6, max_length=100)

class PermissionUpdate(BaseModel):
    role: str
    module: str
    can_view: bool = True
    can_create: bool = False
    can_edit: bool = False
    can_delete: bool = False


def admin_only(user: User):
    if user.role != "ADMINISTRADOR":
        raise HTTPException(403, "Apenas administradores podem acessar este recurso.")


def audit(db, user, action, description):
    db.add(AuditLog(username=user.username, action=action, description=description))


def user_dict(u):
    return {"id": u.id, "username": u.username, "name": u.name, "role": u.role, "active": u.active, "created_at": u.created_at}

@router.get("/overview")
def overview(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    users = db.query(User).count()
    active = db.query(User).filter(User.active.is_(True)).count()
    audits = db.query(AuditLog).count()
    permissions = db.query(Permission).count()
    return {"users": users, "active_users": active, "audit_events": audits, "permissions": permissions, "roles": ROLES, "modules": MODULES}

@router.get("/users")
def users(q: str = "", db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    query = db.query(User)
    if q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(User.username.ilike(term), User.name.ilike(term), User.role.ilike(term)))
    return [user_dict(x) for x in query.order_by(User.name).all()]

@router.post("/users")
def create_user(data: UserCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    role = data.role.upper()
    if role not in ROLES:
        raise HTTPException(400, "Perfil inválido.")
    if db.query(User).filter(User.username == data.username.strip()).first():
        raise HTTPException(409, "Usuário já existe.")
    obj = User(username=data.username.strip(), name=data.name.strip(), password_hash=hash_password(data.password), role=role, active=data.active)
    db.add(obj); db.flush(); audit(db, user, "CREATE_USER", f"Usuário {obj.username} criado com perfil {obj.role}."); db.commit(); db.refresh(obj)
    return user_dict(obj)

@router.patch("/users/{user_id}")
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    obj = db.get(User, user_id)
    if not obj: raise HTTPException(404, "Usuário não encontrado.")
    if data.role is not None:
        role = data.role.upper()
        if role not in ROLES: raise HTTPException(400, "Perfil inválido.")
        obj.role = role
    if data.name is not None: obj.name = data.name.strip()
    if data.active is not None:
        if obj.id == user.id and not data.active: raise HTTPException(400, "O administrador atual não pode se desativar.")
        obj.active = data.active
    audit(db, user, "UPDATE_USER", f"Usuário {obj.username} atualizado."); db.commit(); db.refresh(obj)
    return user_dict(obj)

@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: int, data: PasswordChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    obj = db.get(User, user_id)
    if not obj: raise HTTPException(404, "Usuário não encontrado.")
    obj.password_hash = hash_password(data.new_password)
    audit(db, user, "RESET_PASSWORD", f"Senha do usuário {obj.username} redefinida por administrador."); db.commit()
    return {"message": "Senha redefinida com sucesso."}

@router.post("/password")
def change_password(data: PasswordChange, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(400, "A senha atual está incorreta.")
    user.password_hash = hash_password(data.new_password)
    audit(db, user, "CHANGE_PASSWORD", "Usuário alterou a própria senha."); db.commit()
    return {"message": "Senha alterada. Faça login novamente se a sessão atual for encerrada."}

@router.get("/permissions")
def permissions(role: str | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    q = db.query(Permission)
    if role: q = q.filter(Permission.role == role.upper())
    rows = q.order_by(Permission.role, Permission.module).all()
    return [{"id": x.id, "role": x.role, "module": x.module, "can_view": x.can_view, "can_create": x.can_create, "can_edit": x.can_edit, "can_delete": x.can_delete} for x in rows]

@router.put("/permissions")
def save_permission(data: PermissionUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    role, module = data.role.upper(), data.module.upper()
    if role not in ROLES or module not in MODULES: raise HTTPException(400, "Perfil ou módulo inválido.")
    obj = db.query(Permission).filter(Permission.role == role, Permission.module == module).first()
    if not obj:
        obj = Permission(role=role, module=module); db.add(obj)
    obj.can_view, obj.can_create, obj.can_edit, obj.can_delete = data.can_view, data.can_create, data.can_edit, data.can_delete
    audit(db, user, "UPDATE_PERMISSION", f"Permissão {role}/{module} atualizada."); db.commit(); db.refresh(obj)
    return {"id": obj.id, "role": obj.role, "module": obj.module, "can_view": obj.can_view, "can_create": obj.can_create, "can_edit": obj.can_edit, "can_delete": obj.can_delete}

@router.get("/audit")
def audit_history(q: str = "", action: str = "", username: str = "", days: int = Query(30, ge=1, le=3650), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    since = datetime.utcnow() - timedelta(days=days)
    query = db.query(AuditLog).filter(AuditLog.created_at >= since)
    if q.strip():
        term = f"%{q.strip()}%"
        query = query.filter(or_(AuditLog.description.ilike(term), AuditLog.action.ilike(term)))
    if action: query = query.filter(AuditLog.action == action)
    if username: query = query.filter(AuditLog.username == username)
    rows = query.order_by(desc(AuditLog.created_at)).limit(limit).all()
    return [{"id": x.id, "username": x.username, "action": x.action, "description": x.description, "created_at": x.created_at} for x in rows]

@router.get("/settings")
def settings(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    return [{"key": x.key, "value": x.value} for x in db.query(Setting).order_by(Setting.key).all()]

@router.put("/settings/{key}")
def update_setting(key: str, value: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    admin_only(user)
    obj = db.query(Setting).filter(Setting.key == key).first()
    if not obj: obj = Setting(key=key, value=value); db.add(obj)
    else: obj.value = value
    audit(db, user, "UPDATE_SETTING", f"Configuração {key} alterada."); db.commit()
    return {"key": key, "value": value}
