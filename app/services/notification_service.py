"""
Servicio de notificaciones y alertas
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.notification import Notification, NotificationType, NotificationChannel, NotificationStatus
from app.models.user import User
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    """Servicio para manejo de notificaciones"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self,
        title: str,
        message: str,
        notification_type: NotificationType,
        channel: NotificationChannel,
        user_id: int,
        priority: int = 1,
        notification_metadata: dict = None,
        scheduled_at: datetime = None
    ) -> Notification:
        """Crear nueva notificación"""
        notification = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            user_id=user_id,
            priority=priority,
            notification_metadata=notification_metadata or {},
            scheduled_at=scheduled_at
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def send_notification(self, notification_id: int) -> bool:
        """Enviar notificación (mock implementation)"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id
        ).first()
        
        if not notification:
            return False
        
        try:
            # En un sistema real, aquí se enviaría la notificación
            # Por ahora, solo simulamos el envío
            
            if notification.channel == NotificationChannel.EMAIL:
                self._send_email(notification)
            elif notification.channel == NotificationChannel.SMS:
                self._send_sms(notification)
            elif notification.channel == NotificationChannel.PUSH:
                self._send_push(notification)
            elif notification.channel == NotificationChannel.DASHBOARD:
                self._send_dashboard(notification)
            
            # Actualizar estado
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Notification {notification_id} sent successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send notification {notification_id}: {str(e)}")
            notification.status = NotificationStatus.FAILED
            self.db.commit()
            return False
    
    def _send_email(self, notification: Notification):
        """Enviar email (mock)"""
        logger.info(f"Mock email sent to user {notification.user_id}: {notification.title}")
        # En producción: usar SMTP o servicio de email
    
    def _send_sms(self, notification: Notification):
        """Enviar SMS (mock)"""
        logger.info(f"Mock SMS sent to user {notification.user_id}: {notification.title}")
        # En producción: usar servicio de SMS
    
    def _send_push(self, notification: Notification):
        """Enviar push notification (mock)"""
        logger.info(f"Mock push notification sent to user {notification.user_id}: {notification.title}")
        # En producción: usar FCM o similar
    
    def _send_dashboard(self, notification: Notification):
        """Enviar notificación al dashboard (mock)"""
        logger.info(f"Mock dashboard notification for user {notification.user_id}: {notification.title}")
        # En producción: usar WebSockets o Server-Sent Events
    
    def get_user_notifications(
        self,
        user_id: int,
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Notification]:
        """Obtener notificaciones de un usuario"""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        
        if unread_only:
            query = query.filter(Notification.status != NotificationStatus.READ)
        
        return query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """Marcar notificación como leída"""
        notification = self.db.query(Notification).filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        ).first()
        
        if not notification:
            return False
        
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def create_alert_for_incident(self, incident_id: int, incident_title: str, priority: str):
        """Crear alerta para incidente crítico"""
        # Obtener administradores y auditores
        users = self.db.query(User).filter(
            User.role.in_(["admin", "auditor"]),
            User.is_active == True
        ).all()
        
        notification_type = NotificationType.CRITICAL if priority == "critical" else NotificationType.WARNING
        
        for user in users:
            self.create_notification(
                title=f"🚨 Incidente {priority.upper()}: {incident_title}",
                message=f"Se ha registrado un incidente de prioridad {priority}. ID: {incident_id}",
                notification_type=notification_type,
                channel=NotificationChannel.DASHBOARD,
                user_id=user.id,
                priority=5 if priority == "critical" else 3,
                notification_metadata={"incident_id": incident_id, "type": "incident"}
            )
    
    def create_alert_for_non_conformity(self, nc_id: int, nc_title: str, severity: str):
        """Crear alerta para no conformidad crítica"""
        users = self.db.query(User).filter(
            User.role.in_(["admin", "auditor", "gestor"]),
            User.is_active == True
        ).all()
        
        notification_type = NotificationType.CRITICAL if severity == "critical" else NotificationType.WARNING
        
        for user in users:
            self.create_notification(
                title=f"⚠️ No Conformidad {severity.upper()}: {nc_title}",
                message=f"Se ha registrado una no conformidad de severidad {severity}. ID: {nc_id}",
                notification_type=notification_type,
                channel=NotificationChannel.DASHBOARD,
                user_id=user.id,
                priority=5 if severity == "critical" else 3,
                notification_metadata={"non_conformity_id": nc_id, "type": "non_conformity"}
            )
    
    def create_alert_for_document_review(self, doc_id: int, doc_title: str):
        """Crear alerta para documento pendiente de revisión"""
        # Obtener auditores y administradores
        users = self.db.query(User).filter(
            User.role.in_(["admin", "auditor"]),
            User.is_active == True
        ).all()
        
        for user in users:
            self.create_notification(
                title=f"📄 Documento Pendiente de Revisión: {doc_title}",
                message=f"El documento '{doc_title}' está pendiente de revisión y aprobación.",
                notification_type=NotificationType.INFO,
                channel=NotificationChannel.DASHBOARD,
                user_id=user.id,
                priority=2,
                notification_metadata={"document_id": doc_id, "type": "document_review"}
            )
    
    def process_scheduled_notifications(self):
        """Procesar notificaciones programadas (para ejecutar en background)"""
        now = datetime.utcnow()
        scheduled_notifications = self.db.query(Notification).filter(
            Notification.status == NotificationStatus.PENDING,
            Notification.scheduled_at <= now
        ).all()
        
        for notification in scheduled_notifications:
            self.send_notification(notification.id)
    
    def cleanup_old_notifications(self, days: int = 30):
        """Limpiar notificaciones antiguas"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        old_notifications = self.db.query(Notification).filter(
            Notification.created_at < cutoff_date,
            Notification.status == NotificationStatus.READ
        ).all()
        
        for notification in old_notifications:
            self.db.delete(notification)
        
        self.db.commit()
        
        logger.info(f"Cleaned up {len(old_notifications)} old notifications")
