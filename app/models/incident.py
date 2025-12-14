"""
Modelo de Incidente para gestión de incidentes (RF-03)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class IncidentPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentType(str, enum.Enum):
    SYSTEM_FAILURE = "system_failure"
    SECURITY_BREACH = "security_breach"
    DATA_LOSS = "data_loss"
    SERVICE_DISRUPTION = "service_disruption"
    OTHER = "other"

class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    incident_type = Column(Enum(IncidentType), nullable=False)
    priority = Column(Enum(IncidentPriority), nullable=False)
    status = Column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    
    # Detalles del incidente
    impact_description = Column(Text)  # Descripción del impacto
    affected_systems = Column(String(500))  # Sistemas afectados
    business_impact = Column(Text)  # Impacto en el negocio
    resolution_steps = Column(Text)  # Pasos para resolución
    lessons_learned = Column(Text)  # Lecciones aprendidas
    
    # Fechas importantes
    occurred_at = Column(DateTime(timezone=True), nullable=False)
    detected_at = Column(DateTime(timezone=True), nullable=False)
    resolved_at = Column(DateTime(timezone=True))
    closed_at = Column(DateTime(timezone=True))
    
    # Tiempos de respuesta (en minutos)
    response_time = Column(Integer)  # Tiempo de respuesta inicial
    resolution_time = Column(Integer)  # Tiempo total de resolución
    
    # Relaciones
    reported_by = Column(Integer, ForeignKey("users.id"))
    assigned_to = Column(Integer, ForeignKey("users.id"))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    reporter = relationship("User", foreign_keys=[reported_by])
    assignee = relationship("User", foreign_keys=[assigned_to])
    resolver = relationship("User", foreign_keys=[resolved_by])
    
    def __repr__(self):
        return f"<Incident(title='{self.title}', priority='{self.priority}', status='{self.status}')>"

