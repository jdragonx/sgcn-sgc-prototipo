"""
Router para dashboard y estadísticas generales
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.incident import Incident
from app.models.non_conformity import NonConformity
from app.models.audit import Audit
from app.models.kpi import KPI
from app.schemas import DashboardStats
from app.auth import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas del dashboard"""
    
    # Documentos
    total_documents = db.query(Document).count()
    pending_documents = db.query(Document).filter(
        Document.status.in_(["draft", "pending_review"])
    ).count()
    
    # Incidentes
    total_incidents = db.query(Incident).count()
    open_incidents = db.query(Incident).filter(
        Incident.status.in_(["open", "in_progress"])
    ).count()
    
    # No conformidades
    total_non_conformities = db.query(NonConformity).count()
    open_non_conformities = db.query(NonConformity).filter(
        NonConformity.status.in_(["open", "in_progress"])
    ).count()
    
    # Auditorías
    total_audits = db.query(Audit).count()
    planned_audits = db.query(Audit).filter(Audit.status == "planned").count()
    
    # KPIs
    total_kpis = db.query(KPI).count()
    
    # Actividades recientes (últimos 7 días)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    
    recent_activities = []
    
    # Documentos recientes
    recent_docs = db.query(Document).filter(
        Document.created_at >= seven_days_ago
    ).order_by(Document.created_at.desc()).limit(5).all()
    
    for doc in recent_docs:
        recent_activities.append({
            "type": "document",
            "title": doc.title,
            "date": doc.created_at.isoformat(),
            "status": doc.status,
            "user": doc.creator.full_name if doc.creator else "Unknown"
        })
    
    # Incidentes recientes
    recent_incidents = db.query(Incident).filter(
        Incident.created_at >= seven_days_ago
    ).order_by(Incident.created_at.desc()).limit(5).all()
    
    for incident in recent_incidents:
        recent_activities.append({
            "type": "incident",
            "title": incident.title,
            "date": incident.created_at.isoformat(),
            "priority": incident.priority,
            "user": incident.reporter.full_name if incident.reporter else "Unknown"
        })
    
    # No conformidades recientes
    recent_nc = db.query(NonConformity).filter(
        NonConformity.created_at >= seven_days_ago
    ).order_by(NonConformity.created_at.desc()).limit(5).all()
    
    for nc in recent_nc:
        recent_activities.append({
            "type": "non_conformity",
            "title": nc.title,
            "date": nc.created_at.isoformat(),
            "severity": nc.severity,
            "user": nc.reporter.full_name if nc.reporter else "Unknown"
        })
    
    # Ordenar actividades por fecha
    recent_activities.sort(key=lambda x: x["date"], reverse=True)
    recent_activities = recent_activities[:10]  # Top 10 actividades
    
    return DashboardStats(
        total_documents=total_documents,
        pending_documents=pending_documents,
        total_incidents=total_incidents,
        open_incidents=open_incidents,
        total_non_conformities=total_non_conformities,
        open_non_conformities=open_non_conformities,
        total_audits=total_audits,
        planned_audits=planned_audits,
        total_kpis=total_kpis,
        recent_activities=recent_activities
    )

@router.get("/alerts")
def get_dashboard_alerts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener alertas para el dashboard"""
    alerts = []
    
    # Incidentes críticos abiertos
    critical_incidents = db.query(Incident).filter(
        Incident.priority == "critical",
        Incident.status.in_(["open", "in_progress"])
    ).count()
    
    if critical_incidents > 0:
        alerts.append({
            "type": "critical",
            "title": f"{critical_incidents} Incidente(s) Crítico(s) Abierto(s)",
            "message": "Hay incidentes críticos que requieren atención inmediata",
            "count": critical_incidents
        })
    
    # No conformidades críticas abiertas
    critical_nc = db.query(NonConformity).filter(
        NonConformity.severity == "critical",
        NonConformity.status.in_(["open", "in_progress"])
    ).count()
    
    if critical_nc > 0:
        alerts.append({
            "type": "critical",
            "title": f"{critical_nc} No Conformidad(es) Crítica(s) Abierta(s)",
            "message": "Hay no conformidades críticas que requieren acción inmediata",
            "count": critical_nc
        })
    
    # Documentos pendientes de revisión
    pending_review = db.query(Document).filter(
        Document.status == "pending_review"
    ).count()
    
    if pending_review > 0:
        alerts.append({
            "type": "warning",
            "title": f"{pending_review} Documento(s) Pendiente(s) de Revisión",
            "message": "Hay documentos que requieren revisión y aprobación",
            "count": pending_review
        })
    
    # Auditorías próximas a vencer (próximos 7 días)
    seven_days_from_now = datetime.utcnow() + timedelta(days=7)
    upcoming_audits = db.query(Audit).filter(
        Audit.status == "planned",
        Audit.planned_start_date <= seven_days_from_now,
        Audit.planned_start_date >= datetime.utcnow()
    ).count()
    
    if upcoming_audits > 0:
        alerts.append({
            "type": "info",
            "title": f"{upcoming_audits} Auditoría(s) Próxima(s)",
            "message": "Hay auditorías programadas para los próximos 7 días",
            "count": upcoming_audits
        })
    
    return {
        "alerts": alerts,
        "total_alerts": len(alerts),
        "critical_count": len([a for a in alerts if a["type"] == "critical"]),
        "warning_count": len([a for a in alerts if a["type"] == "warning"]),
        "info_count": len([a for a in alerts if a["type"] == "info"])
    }

