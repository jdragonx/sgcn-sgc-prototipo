"""
Router para gestión de incidentes (RF-03)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.incident import Incident
from app.schemas import IncidentCreate, IncidentUpdate, Incident as IncidentSchema, MessageResponse
from app.auth import get_current_active_user
from datetime import datetime

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("/", response_model=IncidentSchema)
def create_incident(
    incident: IncidentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo incidente"""
    db_incident = Incident(
        title=incident.title,
        description=incident.description,
        incident_type=incident.incident_type,
        priority=incident.priority,
        impact_description=incident.impact_description,
        affected_systems=incident.affected_systems,
        occurred_at=incident.occurred_at,
        detected_at=incident.detected_at,
        reported_by=current_user.id
    )
    
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    return db_incident

@router.get("/", response_model=List[IncidentSchema])
def get_incidents(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    priority_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de incidentes con filtros opcionales"""
    query = db.query(Incident)
    
    if status_filter:
        query = query.filter(Incident.status == status_filter)
    if priority_filter:
        query = query.filter(Incident.priority == priority_filter)
    
    incidents = query.offset(skip).limit(limit).all()
    return incidents

@router.get("/{incident_id}", response_model=IncidentSchema)
def get_incident(
    incident_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener incidente por ID"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.put("/{incident_id}", response_model=IncidentSchema)
def update_incident(
    incident_id: int,
    incident_update: IncidentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar incidente"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Solo el reportero, asignado o admin puede editar
    can_edit = (
        incident.reported_by == current_user.id or
        incident.assigned_to == current_user.id or
        current_user.role.value == "admin"
    )
    
    if not can_edit:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = incident_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(incident, field, value)
    
    incident.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(incident)
    
    return incident

@router.post("/{incident_id}/assign", response_model=IncidentSchema)
def assign_incident(
    incident_id: int,
    assignee_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Asignar incidente a un usuario"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Verificar que el asignado existe
    assignee = db.query(User).filter(User.id == assignee_id).first()
    if not assignee:
        raise HTTPException(status_code=404, detail="Assignee not found")
    
    incident.assigned_to = assignee_id
    incident.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(incident)
    
    return incident

@router.post("/{incident_id}/resolve", response_model=IncidentSchema)
def resolve_incident(
    incident_id: int,
    resolution_steps: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Resolver incidente"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    incident.status = "resolved"
    incident.resolution_steps = resolution_steps
    incident.resolved_by = current_user.id
    incident.resolved_at = datetime.utcnow()
    incident.updated_at = datetime.utcnow()
    
    # Calcular tiempo de resolución
    if incident.detected_at:
        time_diff = incident.resolved_at - incident.detected_at
        incident.resolution_time = int(time_diff.total_seconds() / 60)  # en minutos
    
    db.commit()
    db.refresh(incident)
    
    return incident

@router.post("/{incident_id}/close", response_model=IncidentSchema)
def close_incident(
    incident_id: int,
    lessons_learned: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cerrar incidente"""
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    if incident.status != "resolved":
        raise HTTPException(status_code=400, detail="Incident must be resolved before closing")
    
    incident.status = "closed"
    incident.lessons_learned = lessons_learned
    incident.closed_at = datetime.utcnow()
    incident.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(incident)
    
    return incident

@router.get("/stats/summary")
def get_incident_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de incidentes"""
    total_incidents = db.query(Incident).count()
    open_incidents = db.query(Incident).filter(Incident.status == "open").count()
    in_progress_incidents = db.query(Incident).filter(Incident.status == "in_progress").count()
    resolved_incidents = db.query(Incident).filter(Incident.status == "resolved").count()
    closed_incidents = db.query(Incident).filter(Incident.status == "closed").count()
    
    # Incidentes por prioridad
    critical_incidents = db.query(Incident).filter(Incident.priority == "critical").count()
    high_incidents = db.query(Incident).filter(Incident.priority == "high").count()
    medium_incidents = db.query(Incident).filter(Incident.priority == "medium").count()
    low_incidents = db.query(Incident).filter(Incident.priority == "low").count()
    
    return {
        "total_incidents": total_incidents,
        "by_status": {
            "open": open_incidents,
            "in_progress": in_progress_incidents,
            "resolved": resolved_incidents,
            "closed": closed_incidents
        },
        "by_priority": {
            "critical": critical_incidents,
            "high": high_incidents,
            "medium": medium_incidents,
            "low": low_incidents
        }
    }

