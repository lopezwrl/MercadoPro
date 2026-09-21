from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
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
