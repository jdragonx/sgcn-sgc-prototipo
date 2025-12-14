"""
Modelo de No Conformidad (RF-02)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class NonConformityStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class NonConformitySeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NonConformity(Base):
    __tablename__ = "non_conformities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum(NonConformitySeverity), nullable=False)
    status = Column(Enum(NonConformityStatus), default=NonConformityStatus.OPEN)
    
    # Detalles del problema
    location = Column(String(200))  # Ubicación donde ocurrió
    process_affected = Column(String(200))  # Proceso afectado
    root_cause = Column(Text)  # Causa raíz identificada
    corrective_action = Column(Text)  # Acción correctiva
    preventive_action = Column(Text)  # Acción preventiva
    
    # Fechas importantes
    detected_date = Column(DateTime(timezone=True), nullable=False)
    target_resolution_date = Column(DateTime(timezone=True))
    actual_resolution_date = Column(DateTime(timezone=True))
    
    # Relaciones
    reported_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    closed_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reporter = relationship("User", foreign_keys=[reported_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
    closer = relationship("User", foreign_keys=[closed_by])
    
    def __repr__(self):
        return f"<NonConformity(title='{self.title}', severity='{self.severity}', status='{self.status}')>"

