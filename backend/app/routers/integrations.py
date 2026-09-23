from datetime import datetime
import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import IntegrationConfig, HardwareDevice, AuditLog, User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/integrations", tags=["Integrações"])

TYPES = ["SCANNER", "IMPRESSORA", "GAVETA", "BALANCA"]
KEYS = ["FISCAL", "IMPRESSAO", "SCANNER", "BALANCA"]

def admin(user):
    if user.role != "ADMINISTRADOR":
        raise HTTPException(403, "Apenas administradores podem configurar integrações.")

def audit(db, user, action, desc):
    db.add(AuditLog(username=user.username, action=action, description=desc))

class IntegrationUpdate(BaseModel):
    provider: str = "LOCAL"
    environment: str = "HOMOLOGACAO"
    active: bool = False
    config: dict = Field(default_factory=dict)

class DeviceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    device_type: str
    connection: str = "BROWSER"
    address: str | None = None
    active: bool = True
    notes: str | None = None

class DeviceUpdate(DeviceCreate):
    pass

def cfg_dict(x):
    try: return json.loads(x.config_json or "{}")
    except Exception: return {}

def cfg_out(x):
    return {"id":x.id,"key":x.key,"provider":x.provider,"environment":x.environment,"active":x.active,"status":x.status,"config":cfg_dict(x),"updated_at":x.updated_at}

def dev_out(x):
    return {"id":x.id,"name":x.name,"device_type":x.device_type,"connection":x.connection,"address":x.address,"active":x.active,"last_test":x.last_test,"status":x.status,"notes":x.notes}

@router.get("/overview")
def overview(db: Session=Depends(get_db), user: User=Depends(get_current_user)):
    admin(user)
    configs={x.key:cfg_out(x) for x in db.query(IntegrationConfig).all()}
    devices=[dev_out(x) for x in db.query(HardwareDevice).order_by(HardwareDevice.name).all()]
    return {"configs":configs,"devices":devices,"fiscal_note":"A emissão fiscal real depende de certificado digital, credenciais, UF e integração homologada; esta fase prepara o núcleo sem simular autorização da SEFAZ."}

@router.put("/config/{key}")
def save_config(key:str, data:IntegrationUpdate, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    admin(user)
    key=key.upper()
    if key not in KEYS: raise HTTPException(400,"Integração inválida.")
    env=data.environment.upper()
    if env not in ("HOMOLOGACAO","PRODUCAO"): raise HTTPException(400,"Ambiente inválido.")
    # Never accept common secret fields for persistence in this generic config.
    safe=dict(data.config)
    for secret in ("password","senha","secret","token","certificate_password","senha_certificado"):
        safe.pop(secret,None)
    obj=db.query(IntegrationConfig).filter(IntegrationConfig.key==key).first()
    if not obj:
        obj=IntegrationConfig(key=key); db.add(obj)
    obj.provider=data.provider.strip()[:80] or "LOCAL"; obj.environment=env; obj.active=data.active; obj.status="CONFIGURADO" if data.active else "INATIVO"; obj.config_json=json.dumps(safe,ensure_ascii=False)
    audit(db,user,"UPDATE_INTEGRATION",f"Integração {key} atualizada."); db.commit(); db.refresh(obj)
    return cfg_out(obj)

@router.post("/devices")
def create_device(data:DeviceCreate, db:Session=Depends(get_db), user:User=Depends(get_current_user)):
    admin(user)
    typ=data.device_type.upper()
    if typ not in TYPES: raise HTTPException(400,"Tipo de equipamento inválido.")
    obj=HardwareDevice(name=data.name.strip(),device_type=typ,connection=data.connection.upper(),address=data.address,active=data.active,notes=data.notes)
    db.add(obj); audit(db,user,"CREATE_DEVICE",f"Equipamento {obj.name} cadastrado."); db.commit(); db.refresh(obj)
    return dev_out(obj)

@router.patch("/devices/{device_id}")
def update_device(device_id:int,data:DeviceUpdate,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    admin(user); obj=db.get(HardwareDevice,device_id)
    if not obj: raise HTTPException(404,"Equipamento não encontrado.")
    typ=data.device_type.upper()
    if typ not in TYPES: raise HTTPException(400,"Tipo de equipamento inválido.")
    obj.name=data.name.strip(); obj.device_type=typ; obj.connection=data.connection.upper(); obj.address=data.address; obj.active=data.active; obj.notes=data.notes
    audit(db,user,"UPDATE_DEVICE",f"Equipamento {obj.name} atualizado."); db.commit(); db.refresh(obj)
    return dev_out(obj)

@router.post("/devices/{device_id}/test")
def test_device(device_id:int,db:Session=Depends(get_db),user:User=Depends(get_current_user)):
    admin(user); obj=db.get(HardwareDevice,device_id)
    if not obj: raise HTTPException(404,"Equipamento não encontrado.")
    obj.last_test=datetime.utcnow(); obj.status="TESTE_LOCAL" if obj.connection in ("BROWSER","USB") else "ENDERECO_VALIDADO"
    audit(db,user,"TEST_DEVICE",f"Teste do equipamento {obj.name}: {obj.status}."); db.commit(); db.refresh(obj)
    return {**dev_out(obj),"message":"Teste de configuração registrado. A comunicação física efetiva depende do driver/equipamento disponível no computador do caixa."}
