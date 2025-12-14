"""
Modelo de Control de Cambios (RF-07)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class ChangeStatus(str, enum.Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class ChangeType(str, enum.Enum):
    PROCESS = "process"
    DOCUMENT = "document"
    SYSTEM = "system"
    PROCEDURE = "procedure"
    POLICY = "policy"

class ChangePriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ChangeControl(Base):
    __tablename__ = "change_controls"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    change_type = Column(Enum(ChangeType), nullable=False)
    priority = Column(Enum(ChangePriority), nullable=False)
    status = Column(Enum(ChangeStatus), default=ChangeStatus.REQUESTED)
    
    # Detalles del cambio
    current_state = Column(Text)  # Estado actual
    proposed_state = Column(Text)  # Estado propuesto
    justification = Column(Text)  # Justificación del cambio
    impact_analysis = Column(Text)  # Análisis de impacto
    risk_assessment = Column(Text)  # Evaluación de riesgos
    
    # Plan de implementación
    implementation_plan = Column(Text)
    rollback_plan = Column(Text)
    testing_plan = Column(Text)
    
    # Fechas
    requested_date = Column(DateTime(timezone=True), nullable=False)
    planned_implementation_date = Column(DateTime(timezone=True))
    actual_implementation_date = Column(DateTime(timezone=True))
    completion_date = Column(DateTime(timezone=True))
    
    # Relaciones
    requested_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    implemented_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    requester = relationship("User", foreign_keys=[requested_by])
    approver = relationship("User", foreign_keys=[approved_by])
    implementer = relationship("User", foreign_keys=[implemented_by])
    
    def __repr__(self):
        return f"<ChangeControl(title='{self.title}', type='{self.change_type}', status='{self.status}')>"

