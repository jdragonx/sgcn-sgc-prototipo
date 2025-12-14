"""
Router para gestión de KPIs y métricas (RF-08)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.kpi import KPI, KPIMeasurement
from app.schemas import KPICreate, KPIUpdate, KPI as KPISchema, KPIMeasurementCreate, KPIMeasurement as KPIMeasurementSchema, MessageResponse
from app.auth import get_current_active_user, require_role
from datetime import datetime, timedelta

router = APIRouter(prefix="/kpis", tags=["kpis"])

@router.post("/", response_model=KPISchema)
def create_kpi(
    kpi: KPICreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo KPI"""
    db_kpi = KPI(
        name=kpi.name,
        description=kpi.description,
        kpi_type=kpi.kpi_type,
        measurement_unit=kpi.measurement_unit,
        target_value=kpi.target_value,
        minimum_value=kpi.minimum_value,
        maximum_value=kpi.maximum_value,
        measurement_frequency=kpi.measurement_frequency,
        owner=current_user.id
    )
    
    db.add(db_kpi)
    db.commit()
    db.refresh(db_kpi)
    
    return db_kpi

@router.get("/", response_model=List[KPISchema])
def get_kpis(
    skip: int = 0,
    limit: int = 100,
    type_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de KPIs con filtros opcionales"""
    query = db.query(KPI)
    
    if type_filter:
        query = query.filter(KPI.kpi_type == type_filter)
    
    kpis = query.offset(skip).limit(limit).all()
    return kpis

@router.get("/{kpi_id}", response_model=KPISchema)
def get_kpi(
    kpi_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener KPI por ID"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    return kpi

@router.put("/{kpi_id}", response_model=KPISchema)
def update_kpi(
    kpi_id: int,
    kpi_update: KPIUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar KPI"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    # Solo el propietario o admin puede editar
    can_edit = (
        kpi.owner == current_user.id or
        current_user.role.value == "admin"
    )
    
    if not can_edit:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = kpi_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(kpi, field, value)
    
    kpi.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(kpi)
    
    return kpi

@router.delete("/{kpi_id}", response_model=MessageResponse)
def delete_kpi(
    kpi_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Eliminar KPI (solo admin)"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    # Eliminar mediciones asociadas
    db.query(KPIMeasurement).filter(KPIMeasurement.kpi_id == kpi_id).delete()
    
    db.delete(kpi)
    db.commit()
    
    return MessageResponse(message="KPI deleted successfully")

@router.post("/{kpi_id}/measurements", response_model=KPIMeasurementSchema)
def add_measurement(
    kpi_id: int,
    measurement: KPIMeasurementCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Agregar medición a un KPI"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    db_measurement = KPIMeasurement(
        kpi_id=kpi_id,
        measured_value=measurement.measured_value,
        measurement_date=measurement.measurement_date,
        notes=measurement.notes,
        data_source=measurement.data_source,
        measured_by=current_user.id
    )
    
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    
    return db_measurement

@router.get("/{kpi_id}/measurements", response_model=List[KPIMeasurementSchema])
def get_measurements(
    kpi_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener mediciones de un KPI"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    measurements = db.query(KPIMeasurement).filter(
        KPIMeasurement.kpi_id == kpi_id
    ).order_by(KPIMeasurement.measurement_date.desc()).offset(skip).limit(limit).all()
    
    return measurements

@router.get("/{kpi_id}/dashboard")
def get_kpi_dashboard(
    kpi_id: int,
    days: int = 30,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener datos del dashboard para un KPI"""
    kpi = db.query(KPI).filter(KPI.id == kpi_id).first()
    if not kpi:
        raise HTTPException(status_code=404, detail="KPI not found")
    
    # Obtener mediciones de los últimos N días
    start_date = datetime.utcnow() - timedelta(days=days)
    measurements = db.query(KPIMeasurement).filter(
        KPIMeasurement.kpi_id == kpi_id,
        KPIMeasurement.measurement_date >= start_date
    ).order_by(KPIMeasurement.measurement_date.asc()).all()
    
    # Calcular estadísticas
    values = [m.measured_value for m in measurements]
    
    stats = {
        "kpi_name": kpi.name,
        "measurement_unit": kpi.measurement_unit,
        "target_value": kpi.target_value,
        "minimum_value": kpi.minimum_value,
        "maximum_value": kpi.maximum_value,
        "current_value": values[-1] if values else None,
        "average_value": sum(values) / len(values) if values else None,
        "min_value": min(values) if values else None,
        "max_value": max(values) if values else None,
        "measurement_count": len(values),
        "trend": "up" if len(values) >= 2 and values[-1] > values[-2] else "down" if len(values) >= 2 else "stable",
        "measurements": [
            {
                "date": m.measurement_date.isoformat(),
                "value": m.measured_value,
                "notes": m.notes
            } for m in measurements
        ]
    }
    
    return stats

@router.get("/stats/summary")
def get_kpi_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas generales de KPIs"""
    total_kpis = db.query(KPI).count()
    
    # KPIs por tipo
    quality_kpis = db.query(KPI).filter(KPI.kpi_type == "quality").count()
    continuity_kpis = db.query(KPI).filter(KPI.kpi_type == "continuity").count()
    performance_kpis = db.query(KPI).filter(KPI.kpi_type == "performance").count()
    compliance_kpis = db.query(KPI).filter(KPI.kpi_type == "compliance").count()
    customer_kpis = db.query(KPI).filter(KPI.kpi_type == "customer").count()
    
    # Total de mediciones
    total_measurements = db.query(KPIMeasurement).count()
    
    # Mediciones de los últimos 30 días
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_measurements = db.query(KPIMeasurement).filter(
        KPIMeasurement.measurement_date >= thirty_days_ago
    ).count()
    
    return {
        "total_kpis": total_kpis,
        "by_type": {
            "quality": quality_kpis,
            "continuity": continuity_kpis,
            "performance": performance_kpis,
            "compliance": compliance_kpis,
            "customer": customer_kpis
        },
        "total_measurements": total_measurements,
        "recent_measurements_30d": recent_measurements
    }

