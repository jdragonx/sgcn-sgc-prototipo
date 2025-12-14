"""
Router para notificaciones y alertas (RF-10)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.notification import Notification, NotificationType, NotificationChannel
from app.schemas import MessageResponse
from app.auth import get_current_active_user
from app.services.notification_service import NotificationService
from datetime import datetime

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/")
def get_notifications(
    limit: int = 50,
    unread_only: bool = False,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener notificaciones del usuario actual"""
    notification_service = NotificationService(db)
    notifications = notification_service.get_user_notifications(
        user_id=current_user.id,
        limit=limit,
        unread_only=unread_only
    )
    
    return {
        "notifications": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "type": n.notification_type,
                "channel": n.channel,
                "status": n.status,
                "priority": n.priority,
                "created_at": n.created_at.isoformat(),
                "read_at": n.read_at.isoformat() if n.read_at else None,
                "metadata": n.notification_metadata
            } for n in notifications
        ],
        "total": len(notifications)
    }

@router.post("/{notification_id}/read", response_model=MessageResponse)
def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Marcar notificación como leída"""
    notification_service = NotificationService(db)
    
    success = notification_service.mark_as_read(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    return MessageResponse(message="Notification marked as read")

@router.post("/mark-all-read", response_model=MessageResponse)
def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Marcar todas las notificaciones como leídas"""
    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status != "read"
    ).all()
    
    for notification in notifications:
        notification.status = "read"
        notification.read_at = datetime.utcnow()
    
    db.commit()
    
    return MessageResponse(message=f"Marked {len(notifications)} notifications as read")

@router.get("/stats")
def get_notification_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de notificaciones"""
    total_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).count()
    
    unread_notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.status != "read"
    ).count()
    
    # Notificaciones por tipo
    critical_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.notification_type == "critical"
    ).count()
    
    warning_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.notification_type == "warning"
    ).count()
    
    info_count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.notification_type == "info"
    ).count()
    
    return {
        "total_notifications": total_notifications,
        "unread_notifications": unread_notifications,
        "by_type": {
            "critical": critical_count,
            "warning": warning_count,
            "info": info_count
        }
    }

@router.post("/test")
def send_test_notification(
    title: str = "Test Notification",
    message: str = "This is a test notification",
    notification_type: str = "info",
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Enviar notificación de prueba (para testing)"""
    notification_service = NotificationService(db)
    
    try:
        notification = notification_service.create_notification(
            title=title,
            message=message,
            notification_type=NotificationType(notification_type),
            channel=NotificationChannel.DASHBOARD,
            user_id=current_user.id,
            priority=1
        )
        
        # Enviar inmediatamente
        notification_service.send_notification(notification.id)
        
        return MessageResponse(message="Test notification sent successfully")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to send test notification: {str(e)}")

@router.delete("/{notification_id}", response_model=MessageResponse)
def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Eliminar notificación"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    db.delete(notification)
    db.commit()
    
    return MessageResponse(message="Notification deleted successfully")
