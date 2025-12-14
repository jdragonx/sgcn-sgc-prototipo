"""
Router para gestión de auditorías internas (RF-06)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.audit import Audit
from app.schemas import AuditCreate, AuditUpdate, Audit as AuditSchema, MessageResponse
from app.auth import get_current_active_user, require_role
from datetime import datetime

router = APIRouter(prefix="/audits", tags=["audits"])

@router.post("/", response_model=AuditSchema)
def create_audit(
    audit: AuditCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nueva auditoría"""
    db_audit = Audit(
        title=audit.title,
        description=audit.description,
        audit_type=audit.audit_type,
        scope=audit.scope,
        objectives=audit.objectives,
        criteria=audit.criteria,
        planned_start_date=audit.planned_start_date,
        planned_end_date=audit.planned_end_date,
        auditor_lead=current_user.id
    )
    
    db.add(db_audit)
    db.commit()
    db.refresh(db_audit)
    
    return db_audit

@router.get("/", response_model=List[AuditSchema])
def get_audits(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    type_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de auditorías con filtros opcionales"""
    query = db.query(Audit)
    
    if status_filter:
        query = query.filter(Audit.status == status_filter)
    if type_filter:
        query = query.filter(Audit.audit_type == type_filter)
    
    audits = query.offset(skip).limit(limit).all()
    return audits

@router.get("/{audit_id}", response_model=AuditSchema)
def get_audit(
    audit_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener auditoría por ID"""
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit

@router.put("/{audit_id}", response_model=AuditSchema)
def update_audit(
    audit_id: int,
    audit_update: AuditUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar auditoría"""
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    # Solo el auditor líder o admin puede editar
    can_edit = (
        audit.auditor_lead == current_user.id or
        current_user.role.value == "admin"
    )
    
    if not can_edit:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = audit_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(audit, field, value)
    
    audit.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(audit)
    
    return audit

@router.post("/{audit_id}/start", response_model=AuditSchema)
def start_audit(
    audit_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Iniciar auditoría"""
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    if audit.status != "planned":
        raise HTTPException(status_code=400, detail="Audit must be in planned status to start")
    
    audit.status = "in_progress"
    audit.actual_start_date = datetime.utcnow()
    audit.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(audit)
    
    return audit

@router.post("/{audit_id}/complete", response_model=AuditSchema)
def complete_audit(
    audit_id: int,
    findings_count: int = 0,
    non_conformities_count: int = 0,
    observations_count: int = 0,
    recommendations_count: int = 0,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Completar auditoría"""
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    if audit.status != "in_progress":
        raise HTTPException(status_code=400, detail="Audit must be in progress to complete")
    
    audit.status = "completed"
    audit.actual_end_date = datetime.utcnow()
    audit.findings_count = findings_count
    audit.non_conformities_count = non_conformities_count
    audit.observations_count = observations_count
    audit.recommendations_count = recommendations_count
    audit.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(audit)
    
    return audit

@router.post("/{audit_id}/cancel", response_model=AuditSchema)
def cancel_audit(
    audit_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Cancelar auditoría (solo admin)"""
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    audit.status = "cancelled"
    audit.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(audit)
    
    return audit

@router.get("/stats/summary")
def get_audit_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de auditorías"""
    total_audits = db.query(Audit).count()
    planned_audits = db.query(Audit).filter(Audit.status == "planned").count()
    in_progress_audits = db.query(Audit).filter(Audit.status == "in_progress").count()
    completed_audits = db.query(Audit).filter(Audit.status == "completed").count()
    cancelled_audits = db.query(Audit).filter(Audit.status == "cancelled").count()
    
    # Auditorías por tipo
    internal_audits = db.query(Audit).filter(Audit.audit_type == "internal").count()
    external_audits = db.query(Audit).filter(Audit.audit_type == "external").count()
    follow_up_audits = db.query(Audit).filter(Audit.audit_type == "follow_up").count()
    special_audits = db.query(Audit).filter(Audit.audit_type == "special").count()
    
    return {
        "total_audits": total_audits,
        "by_status": {
            "planned": planned_audits,
            "in_progress": in_progress_audits,
            "completed": completed_audits,
            "cancelled": cancelled_audits
        },
        "by_type": {
            "internal": internal_audits,
            "external": external_audits,
            "follow_up": follow_up_audits,
            "special": special_audits
        }
    }

