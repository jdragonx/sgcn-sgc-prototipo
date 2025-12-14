"""
Router para gestión de no conformidades (RF-02)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.non_conformity import NonConformity
from app.schemas import NonConformityCreate, NonConformityUpdate, NonConformity as NonConformitySchema, MessageResponse
from app.auth import get_current_active_user
from datetime import datetime

router = APIRouter(prefix="/non-conformities", tags=["non-conformities"])

@router.post("/", response_model=NonConformitySchema)
def create_non_conformity(
    non_conformity: NonConformityCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nueva no conformidad"""
    db_non_conformity = NonConformity(
        title=non_conformity.title,
        description=non_conformity.description,
        severity=non_conformity.severity,
        location=non_conformity.location,
        process_affected=non_conformity.process_affected,
        detected_date=non_conformity.detected_date,
        reported_by=current_user.id
    )
    
    db.add(db_non_conformity)
    db.commit()
    db.refresh(db_non_conformity)
    
    return db_non_conformity

@router.get("/", response_model=List[NonConformitySchema])
def get_non_conformities(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    severity_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de no conformidades con filtros opcionales"""
    query = db.query(NonConformity)
    
    if status_filter:
        query = query.filter(NonConformity.status == status_filter)
    if severity_filter:
        query = query.filter(NonConformity.severity == severity_filter)
    
    non_conformities = query.offset(skip).limit(limit).all()
    return non_conformities

@router.get("/{non_conformity_id}", response_model=NonConformitySchema)
def get_non_conformity(
    non_conformity_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener no conformidad por ID"""
    non_conformity = db.query(NonConformity).filter(NonConformity.id == non_conformity_id).first()
    if not non_conformity:
        raise HTTPException(status_code=404, detail="Non-conformity not found")
    return non_conformity

@router.put("/{non_conformity_id}", response_model=NonConformitySchema)
def update_non_conformity(
    non_conformity_id: int,
    non_conformity_update: NonConformityUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar no conformidad"""
    non_conformity = db.query(NonConformity).filter(NonConformity.id == non_conformity_id).first()
    if not non_conformity:
        raise HTTPException(status_code=404, detail="Non-conformity not found")
    
    # Solo el reportero, asignado o admin puede editar
    can_edit = (
        non_conformity.reported_by == current_user.id or
        non_conformity.assigned_to == current_user.id or
        current_user.role.value == "admin"
    )
    
    if not can_edit:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = non_conformity_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(non_conformity, field, value)
    
    non_conformity.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(non_conformity)
    
    return non_conformity

@router.post("/{non_conformity_id}/assign", response_model=NonConformitySchema)
def assign_non_conformity(
    non_conformity_id: int,
    assignee_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Asignar no conformidad a un usuario"""
    non_conformity = db.query(NonConformity).filter(NonConformity.id == non_conformity_id).first()
    if not non_conformity:
        raise HTTPException(status_code=404, detail="Non-conformity not found")
    
    # Verificar que el asignado existe
    assignee = db.query(User).filter(User.id == assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    non_conformity.assigned_to = assignee_id
    non_conformity.status = "in_progress"
    non_conformity.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(non_conformity)
    
    return non_conformity

@router.post("/{non_conformity_id}/close", response_model=NonConformitySchema)
def close_non_conformity(
    non_conformity_id: int,
    root_cause: str,
    corrective_action: str,
    preventive_action: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cerrar no conformidad con acciones correctivas"""
    non_conformity = db.query(NonConformity).filter(NonConformity.id == non_conformity_id).first()
    if not non_conformity:
        raise HTTPException(status_code=404, detail="Non-conformity not found")
    
    non_conformity.status = "closed"
    non_conformity.root_cause = root_cause
    non_conformity.corrective_action = corrective_action
    non_conformity.preventive_action = preventive_action
    non_conformity.closed_by = current_user.id
    non_conformity.actual_resolution_date = datetime.utcnow()
    non_conformity.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(non_conformity)
    
    return non_conformity

@router.get("/stats/summary")
def get_non_conformity_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de no conformidades"""
    total_nc = db.query(NonConformity).count()
    open_nc = db.query(NonConformity).filter(NonConformity.status == "open").count()
    in_progress_nc = db.query(NonConformity).filter(NonConformity.status == "in_progress").count()
    closed_nc = db.query(NonConformity).filter(NonConformity.status == "closed").count()
    
    # No conformidades por severidad
    critical_nc = db.query(NonConformity).filter(NonConformity.severity == "critical").count()
    high_nc = db.query(NonConformity).filter(NonConformity.severity == "high").count()
    medium_nc = db.query(NonConformity).filter(NonConformity.severity == "medium").count()
    low_nc = db.query(NonConformity).filter(NonConformity.severity == "low").count()
    
    return {
        "total_non_conformities": total_nc,
        "by_status": {
            "open": open_nc,
            "in_progress": in_progress_nc,
            "closed": closed_nc
        },
        "by_severity": {
            "critical": critical_nc,
            "high": high_nc,
            "medium": medium_nc,
            "low": low_nc
        }
    }

