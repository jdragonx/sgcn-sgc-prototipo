"""
Modelo de Usuario para el sistema SGCN-SGC
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.models.database import Base
import enum

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    GESTOR = "gestor"
    OPERADOR = "operador"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    hashed_password = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.OPERADOR)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role}')>"

