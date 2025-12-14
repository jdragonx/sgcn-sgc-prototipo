"""
Modelos para Continuidad del Negocio (RF-04, RF-05)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class SimulationStatus(str, enum.Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PlanStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    TESTED = "tested"
    OBSOLETE = "obsolete"

class BusinessContinuityPlan(Base):
    __tablename__ = "business_continuity_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(PlanStatus), default=PlanStatus.DRAFT)
    
    # Detalles del plan
    scope = Column(Text)  # Alcance del plan
    objectives = Column(Text)  # Objetivos
    recovery_time_objective = Column(Integer)  # RTO en horas
    recovery_point_objective = Column(Integer)  # RPO en horas
    
    # Fechas
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_tested = Column(DateTime(timezone=True))
    next_review = Column(DateTime(timezone=True))
    
    # Relaciones
    created_by = Column(Integer, ForeignKey("users.id"))
    owner = Column(Integer, ForeignKey("users.id"))
    
    # Relaciones
    creator = relationship("User", foreign_keys=[created_by])
    plan_owner = relationship("User", foreign_keys=[owner])
    
    def __repr__(self):
        return f"<BusinessContinuityPlan(title='{self.title}', status='{self.status}')>"

class EmergencySimulation(Base):
    __tablename__ = "emergency_simulations"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(Enum(SimulationStatus), default=SimulationStatus.PLANNED)
    
    # Detalles de la simulación
    scenario = Column(Text)  # Escenario simulado
    objectives = Column(Text)  # Objetivos de la simulación
    participants = Column(Text)  # Participantes
    
    # Fechas
    planned_date = Column(DateTime(timezone=True))
    actual_date = Column(DateTime(timezone=True))
    duration_hours = Column(Integer)  # Duración en horas
    
    # Resultados
    success_rate = Column(Integer)  # Porcentaje de éxito
    lessons_learned = Column(Text)
    improvement_actions = Column(Text)
    
    # Relaciones
    created_by = Column(Integer, ForeignKey("users.id"))
    coordinator = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    creator = relationship("User", foreign_keys=[created_by])
    simulation_coordinator = relationship("User", foreign_keys=[coordinator])
    
    def __repr__(self):
        return f"<EmergencySimulation(title='{self.title}', status='{self.status}')>"

