from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, Integer, String, Text, ForeignKey, Numeric, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(120))
    role: Mapped[str] = mapped_column(String(30), default="CAIXA", index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Permission(Base):
    __tablename__ = "permissoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    role: Mapped[str] = mapped_column(String(30), index=True)
    module: Mapped[str] = mapped_column(String(50), index=True)
    can_view: Mapped[bool] = mapped_column(Boolean, default=True)
    can_create: Mapped[bool] = mapped_column(Boolean, default=False)
    can_edit: Mapped[bool] = mapped_column(Boolean, default=False)
    can_delete: Mapped[bool] = mapped_column(Boolean, default=False)

class Setting(Base):
    __tablename__ = "configuracoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text)

class AuditLog(Base):
    __tablename__ = "auditoria"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True)
    action: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    subcategories = relationship("Subcategory", back_populates="category")

class Subcategory(Base):
    __tablename__ = "subcategories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    category = relationship("Category", back_populates="subcategories")
    __table_args__ = (Index("ix_subcategories_category_name", "category_id", "name", unique=True),)

class Brand(Base):
    __tablename__ = "brands"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Unit(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(60))
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    internal_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    barcode: Mapped[str | None] = mapped_column(String(50), unique=True, index=True, nullable=True)
    description: Mapped[str] = mapped_column(String(180), index=True)
    short_description: Mapped[str | None] = mapped_column(String(80), nullable=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), index=True)
    subcategory_id: Mapped[int | None] = mapped_column(ForeignKey("subcategories.id"), index=True, nullable=True)
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"), index=True, nullable=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), index=True)
    cost_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    sale_price: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    margin: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=0)
    current_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0)
    min_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0)
    max_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0)
    supplier_name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    location: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expiry_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = relationship("Category")
    subcategory = relationship("Subcategory")
    brand = relationship("Brand")
    unit = relationship("Unit")

class Inventory(Base):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), unique=True, index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3), default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    product = relationship("Product")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3))
    movement_type: Mapped[str] = mapped_column(String(20), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    previous_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3))
    resulting_stock: Mapped[Decimal] = mapped_column(Numeric(14, 3))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    product = relationship("Product")
    user = relationship("User")

class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    trade_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    cnpj: Mapped[str | None] = mapped_column(String(20), unique=True, index=True, nullable=True)
    rg: Mapped[str | None] = mapped_column(String(30), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), index=True, nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(160), nullable=True)
    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    street: Mapped[str | None] = mapped_column(String(180), nullable=True)
    number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), index=True, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_date: Mapped[date | None] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Sale(Base):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id"), index=True, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    sale_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    status: Mapped[str] = mapped_column(String(20), default="PENDENTE", index=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    discount: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    customer = relationship("Customer")
    user = relationship("User")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    __table_args__ = (Index("ix_sales_date_status", "sale_date", "status"),)

class SaleItem(Base):
    __tablename__ = "sale_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14,3))
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), index=True)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(14,2))
    discount: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")
    unit = relationship("Unit")

class CashRegister(Base):
    __tablename__ = "cash_registers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    opened_by: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    opened_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    opening_amount: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    closed_by: Mapped[int | None] = mapped_column(ForeignKey("usuarios.id"), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    closing_amount: Mapped[Decimal | None] = mapped_column(Numeric(14,2), nullable=True)
    expected_amount: Mapped[Decimal | None] = mapped_column(Numeric(14,2), nullable=True)
    difference: Mapped[Decimal | None] = mapped_column(Numeric(14,2), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="ABERTO", index=True)
    opened_user = relationship("User", foreign_keys=[opened_by])
    closed_user = relationship("User", foreign_keys=[closed_by])

class CashMovement(Base):
    __tablename__ = "cash_movements"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cash_register_id: Mapped[int] = mapped_column(ForeignKey("cash_registers.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    movement_type: Mapped[str] = mapped_column(String(30), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    description: Mapped[str] = mapped_column(String(250))
    sale_id: Mapped[int | None] = mapped_column(ForeignKey("sales.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    cash_register = relationship("CashRegister")
    user = relationship("User")
    sale = relationship("Sale")

class SalePayment(Base):
    __tablename__ = "sale_payments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id", ondelete="CASCADE"), index=True)
    payment_type: Mapped[str] = mapped_column(String(30), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    received_amount: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    change_amount: Mapped[Decimal] = mapped_column(Numeric(14,2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    sale = relationship("Sale")

class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    legal_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    trade_name: Mapped[str] = mapped_column(String(180), index=True)
    cnpj: Mapped[str | None] = mapped_column(String(18), unique=True, index=True, nullable=True)
    state_registration: Mapped[str | None] = mapped_column(String(40), nullable=True)
    cpf: Mapped[str | None] = mapped_column(String(14), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    mobile: Mapped[str | None] = mapped_column(String(30), nullable=True)
    email: Mapped[str | None] = mapped_column(String(160), nullable=True)
    cep: Mapped[str | None] = mapped_column(String(10), nullable=True)
    street: Mapped[str | None] = mapped_column(String(180), nullable=True)
    number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    complement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    neighborhood: Mapped[str | None] = mapped_column(String(100), nullable=True)
    city: Mapped[str | None] = mapped_column(String(100), index=True, nullable=True)
    state: Mapped[str | None] = mapped_column(String(2), index=True, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SupplierProduct(Base):
    __tablename__ = "supplier_products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    supplier_product_code: Mapped[str | None] = mapped_column(String(60), nullable=True)
    negotiated_cost: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    delivery_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    __table_args__ = (Index("uq_supplier_product", "supplier_id", "product_id", unique=True),)
    supplier = relationship("Supplier")
    product = relationship("Product")

class Purchase(Base):
    __tablename__ = "purchases"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    supplier_id: Mapped[int] = mapped_column(ForeignKey("suppliers.id"), index=True)
    purchase_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    status: Mapped[str] = mapped_column(String(20), default="RASCUNHO", index=True)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    surcharge: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    freight: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    supplier = relationship("Supplier")
    user = relationship("User")
    items = relationship("PurchaseItem", back_populates="purchase", cascade="all, delete-orphan")

class PurchaseItem(Base):
    __tablename__ = "purchase_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    purchase_id: Mapped[int] = mapped_column(ForeignKey("purchases.id", ondelete="CASCADE"), index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), index=True)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 3))
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), index=True)
    unit_cost: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    discount: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    surcharge: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    total: Mapped[Decimal] = mapped_column(Numeric(14, 2), default=0)
    lot: Mapped[str | None] = mapped_column(String(80), nullable=True)
    expiry_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product")
    unit = relationship("Unit")

class FinancialCategory(Base):
    __tablename__ = 'financial_categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), index=True)
    entry_type: Mapped[str] = mapped_column(String(20), index=True)  # PAGAR/RECEBER
    active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (Index('uq_fin_category_type', 'name', 'entry_type', unique=True),)

class FinancialEntry(Base):
    __tablename__ = 'financial_entries'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    entry_type: Mapped[str] = mapped_column(String(20), index=True) # PAGAR/RECEBER
    description: Mapped[str] = mapped_column(String(250))
    amount: Mapped[Decimal] = mapped_column(Numeric(14,2))
    due_date: Mapped[date] = mapped_column(index=True)
    category: Mapped[str] = mapped_column(String(100), index=True)
    person: Mapped[str | None] = mapped_column(String(180), nullable=True, index=True)
    reference: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default='PENDENTE', index=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey('usuarios.id'), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User')

class IntegrationConfig(Base):
    __tablename__ = "integracoes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    provider: Mapped[str] = mapped_column(String(80), default="LOCAL")
    environment: Mapped[str] = mapped_column(String(20), default="HOMOLOGACAO")
    active: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(30), default="CONFIGURAR")
    config_json: Mapped[str] = mapped_column(Text, default="{}")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class HardwareDevice(Base):
    __tablename__ = "equipamentos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    device_type: Mapped[str] = mapped_column(String(30), index=True)
    connection: Mapped[str] = mapped_column(String(120), default="BROWSER")
    address: Mapped[str | None] = mapped_column(String(180), nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_test: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="NAO_TESTADO")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
