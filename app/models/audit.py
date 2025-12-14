"""
Modelo de Auditoría Interna (RF-06)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class AuditStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AuditType(str, enum.Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    FOLLOW_UP = "follow_up"
    SPECIAL = "special"

class Audit(Base):
    __tablename__ = "audits"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    audit_type = Column(Enum(AuditType), nullable=False)
    status = Column(Enum(AuditStatus), default=AuditStatus.PLANNED)
    
    # Alcance de la auditoría
    scope = Column(Text)  # Alcance de la auditoría
    objectives = Column(Text)  # Objetivos
    criteria = Column(Text)  # Criterios de auditoría
    
    # Fechas
    planned_start_date = Column(DateTime(timezone=True))
    planned_end_date = Column(DateTime(timezone=True))
    actual_start_date = Column(DateTime(timezone=True))
    actual_end_date = Column(DateTime(timezone=True))
    
    # Resultados
    findings_count = Column(Integer, default=0)
    non_conformities_count = Column(Integer, default=0)
    observations_count = Column(Integer, default=0)
    recommendations_count = Column(Integer, default=0)
    
    # Relaciones
    auditor_lead = Column(Integer, ForeignKey("users.id"))
    auditee = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    lead_auditor = relationship("User", foreign_keys=[auditor_lead])
    auditee_user = relationship("User", foreign_keys=[auditee])
    
    def __repr__(self):
        return f"<Audit(title='{self.title}', type='{self.audit_type}', status='{self.status}')>"

