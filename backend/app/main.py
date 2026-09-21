from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.models import User, Permission, Setting
from app.routers import auth, dashboard

app = FastAPI(title="MercadoPro API", version="1.0.0")

origins = [item.strip() for item in settings.cors_origins.split(",") if item.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            db.add(User(
                username="admin",
                password_hash=hash_password("admin123"),
                name="Administrador",
                role="ADMINISTRADOR",
                active=True
            ))
        if db.query(Setting).count() == 0:
            db.add_all([
                Setting(key="system_name", value="MercadoPro"),
                Setting(key="currency", value="BRL"),
                Setting(key="demo_mode", value="true"),
            ])
        db.commit()
    finally:
        db.close()

@app.get("/")
def root():
    return {"name": "MercadoPro", "version": "1.0.0", "phase": 1}

@app.get("/health")
def health():
    return {"status": "ok"}
