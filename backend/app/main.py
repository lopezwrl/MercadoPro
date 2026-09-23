from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.core.security import hash_password
from app.models.models import User, Permission, Setting, Category, Brand, Unit, Supplier, Customer, FinancialCategory
from app.routers import auth, dashboard
from app.routers.products import router as products_router
from app.routers.purchases import router as purchases_router
from app.routers.sales import router as sales_router
from app.routers.inventory import router as inventory_router
from app.routers.catalog import categories, brands
from app.routers.cash import router as cash_router
from app.routers.finance import router as finance_router
from app.routers.reports import router as reports_router
from app.routers.security import router as security_router
from app.routers.integrations import router as integrations_router

app = FastAPI(title="MercadoPro API", version="9.0.0")
origins=[x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    if request.url.path.startswith("/api"):
        response.headers["Cache-Control"] = "no-store"
    return response
app.include_router(auth.router,prefix="/api")
app.include_router(dashboard.router,prefix="/api")
app.include_router(products_router,prefix="/api")
app.include_router(inventory_router,prefix="/api")
app.include_router(categories)
app.include_router(brands)
app.include_router(purchases_router, prefix="/api")
app.include_router(sales_router, prefix="/api")
app.include_router(cash_router, prefix="/api")
app.include_router(finance_router, prefix="/api")
app.include_router(reports_router, prefix="/api")
app.include_router(security_router, prefix="/api")
app.include_router(integrations_router, prefix="/api")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:
        if not db.query(User).filter(User.username=="admin").first():
            db.add(User(username="admin",password_hash=hash_password("admin123"),name="Administrador",role="ADMINISTRADOR",active=True))
        if db.query(Setting).count()==0:
            db.add_all([Setting(key="system_name",value="MercadoPro"),Setting(key="currency",value="BRL"),Setting(key="demo_mode",value="true")])
        seeds=[(Category,"Bebidas"),(Category,"Mercearia"),(Category,"Limpeza"),(Category,"Higiene")]
        for cls,name in seeds:
            if not db.query(cls).filter(cls.name==name).first(): db.add(cls(name=name))
        for name in ["Coca-Cola","Nestlé","Unilever","Ypê"]:
            if not db.query(Brand).filter(Brand.name==name).first(): db.add(Brand(name=name))
        for code,name in [("UN","Unidade"),("KG","Quilograma"),("L","Litro"),("ML","Mililitro"),("CX","Caixa"),("FD","Fardo"),("PC","Peça")]:
            if not db.query(Unit).filter(Unit.code==code).first(): db.add(Unit(code=code,name=name))
        supplier_seeds=[("FORN001","Fornecedor de Alimentos"),("FORN002","Fornecedor de Bebidas"),("FORN003","Fornecedor de Limpeza")]
        for code,name in [("CLI001","Cliente Balcão"),("CLI002","João da Silva"),("CLI003","Maria da Silva")]:
            if not db.query(Customer).filter(Customer.code==code).first(): db.add(Customer(code=code,name=name,active=True))
        for code,name in supplier_seeds:
            if not db.query(Supplier).filter(Supplier.code==code).first():
                db.add(Supplier(code=code, trade_name=name, legal_name=name, active=True))
        finance_seeds=[("Vendas","RECEBER"),("Serviços","RECEBER"),("Fornecedores","PAGAR"),("Despesas operacionais","PAGAR"),("Impostos","PAGAR"),("Folha","PAGAR")]
        for name,typ in finance_seeds:
            if not db.query(FinancialCategory).filter(FinancialCategory.name==name,FinancialCategory.entry_type==typ).first(): db.add(FinancialCategory(name=name,entry_type=typ))
        db.commit()
    finally: db.close()

@app.get("/")
def root(): return {"name":"MercadoPro","version":"9.0.0","phase":9}
@app.get("/health")
def health(): return {"status":"ok","phase":9}
