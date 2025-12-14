"""
Modelo de KPIs y Métricas (RF-08)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class KPIType(str, enum.Enum):
    QUALITY = "quality"
    CONTINUITY = "continuity"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    CUSTOMER = "customer"

class KPIMeasurementUnit(str, enum.Enum):
    PERCENTAGE = "percentage"
    COUNT = "count"
    HOURS = "hours"
    DAYS = "days"
    CURRENCY = "currency"
    RATIO = "ratio"

class KPI(Base):
    __tablename__ = "kpis"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    kpi_type = Column(Enum(KPIType), nullable=False)
    measurement_unit = Column(Enum(KPIMeasurementUnit), nullable=False)
    
    # Valores objetivo
    target_value = Column(Float)
    minimum_value = Column(Float)
    maximum_value = Column(Float)
    
    # Frecuencia de medición
    measurement_frequency = Column(String(50))  # daily, weekly, monthly, quarterly
    
    # Relaciones
    owner = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    kpi_owner = relationship("User", foreign_keys=[owner])
    
    def __repr__(self):
        return f"<KPI(name='{self.name}', type='{self.kpi_type}')>"

class KPIMeasurement(Base):
    __tablename__ = "kpi_measurements"
    
    id = Column(Integer, primary_key=True, index=True)
    kpi_id = Column(Integer, ForeignKey("kpis.id"))
    measured_value = Column(Float, nullable=False)
    measurement_date = Column(DateTime(timezone=True), nullable=False)
    
    # Metadatos adicionales
    notes = Column(Text)
    data_source = Column(String(200))
    
    # Relaciones
    measured_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    kpi = relationship("KPI")
    measurer = relationship("User", foreign_keys=[measured_by])
    
    def __repr__(self):
        return f"<KPIMeasurement(kpi_id={self.kpi_id}, value={self.measured_value}, date={self.measurement_date})>"

