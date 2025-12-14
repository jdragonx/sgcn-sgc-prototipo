#!/usr/bin/env python3
"""
Script para inicializar datos de prueba en el sistema SGCN-SGC
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.document import Document, DocumentType, DocumentStatus
from app.models.incident import Incident, IncidentType, IncidentPriority, IncidentStatus
from app.models.non_conformity import NonConformity, NonConformitySeverity, NonConformityStatus
from app.models.audit import Audit, AuditType, AuditStatus
from app.models.kpi import KPI, KPIType, KPIMeasurementUnit, KPIMeasurement
from app.models.business_continuity import BusinessContinuityPlan, PlanStatus, EmergencySimulation, SimulationStatus
import hashlib
import base64

def get_password_hash(password: str) -> str:
    """Generar hash de contraseña compatible con el sistema de auth"""
    # Usar SHA256 + salt para compatibilidad
    salt = "sgcn_sgc_salt_2024"
    combined = password + salt
    hash_bytes = hashlib.sha256(combined.encode()).digest()
    return base64.b64encode(hash_bytes).decode()
from datetime import datetime, timedelta
import random

def create_tables():
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas correctamente")

def create_users(db: Session):
    """Crear usuarios de prueba"""
    users_data = [
        {
            "username": "admin",
            "email": "admin@sgcn-sgc.com",
            "full_name": "Administrador del Sistema",
            "password": "admin",
            "role": UserRole.ADMIN
        },
        {
            "username": "auditor1",
            "email": "auditor1@sgcn-sgc.com",
            "full_name": "Juan Pérez - Auditor Interno",
            "password": "auditor",
            "role": UserRole.AUDITOR
        },
        {
            "username": "gestor1",
            "email": "gestor1@sgcn-sgc.com",
            "full_name": "María García - Gestora de Procesos",
            "password": "gestor",
            "role": UserRole.GESTOR
        },
        {
            "username": "operador1",
            "email": "operador1@sgcn-sgc.com",
            "full_name": "Carlos López - Operador Crítico",
            "password": "operador",
            "role": UserRole.OPERADOR
        }
    ]
    
    for user_data in users_data:
        existing_user = db.query(User).filter(User.username == user_data["username"]).first()
        if not existing_user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                full_name=user_data["full_name"],
                hashed_password=get_password_hash(user_data["password"]),
                role=user_data["role"]
            )
            db.add(user)
    
    db.commit()
    print("✅ Usuarios de prueba creados")

def create_documents(db: Session):
    """Crear documentos de prueba"""
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    documents_data = [
        {
            "title": "Manual de Calidad SGCN-SGC",
            "description": "Manual principal del sistema de gestión de calidad",
            "document_type": DocumentType.MANUAL,
            "version": "1.0",
            "status": DocumentStatus.APPROVED
        },
        {
            "title": "Política de Continuidad del Negocio",
            "description": "Política corporativa para la continuidad del negocio",
            "document_type": DocumentType.POLICY,
            "version": "2.1",
            "status": DocumentStatus.APPROVED
        },
        {
            "title": "Procedimiento de Gestión de Incidentes",
            "description": "Procedimiento para el manejo de incidentes críticos",
            "document_type": DocumentType.PROCEDURE,
            "version": "1.3",
            "status": DocumentStatus.PENDING_REVIEW
        },
        {
            "title": "Formulario de No Conformidades",
            "description": "Formulario estándar para reportar no conformidades",
            "document_type": DocumentType.FORM,
            "version": "3.0",
            "status": DocumentStatus.APPROVED
        }
    ]
    
    for doc_data in documents_data:
        existing_doc = db.query(Document).filter(Document.title == doc_data["title"]).first()
        if not existing_doc:
            document = Document(
                title=doc_data["title"],
                description=doc_data["description"],
                document_type=doc_data["document_type"],
                version=doc_data["version"],
                status=doc_data["status"],
                created_by=admin_user.id,
                approved_by=admin_user.id if doc_data["status"] == DocumentStatus.APPROVED else None,
                approved_at=datetime.utcnow() if doc_data["status"] == DocumentStatus.APPROVED else None
            )
            db.add(document)
    
    db.commit()
    print("✅ Documentos de prueba creados")

def create_incidents(db: Session):
    """Crear incidentes de prueba"""
    users = db.query(User).all()
    
    incidents_data = [
        {
            "title": "Falla en servidor principal",
            "description": "El servidor principal experimentó una falla de hardware",
            "incident_type": IncidentType.SYSTEM_FAILURE,
            "priority": IncidentPriority.CRITICAL,
            "status": IncidentStatus.RESOLVED,
            "impact_description": "Servicios críticos no disponibles por 2 horas",
            "affected_systems": "Servidor Web, Base de Datos Principal",
            "occurred_at": datetime.utcnow() - timedelta(days=5),
            "detected_at": datetime.utcnow() - timedelta(days=5, hours=1),
            "resolved_at": datetime.utcnow() - timedelta(days=5, hours=3)
        },
        {
            "title": "Intento de acceso no autorizado",
            "description": "Se detectó un intento de acceso no autorizado al sistema",
            "incident_type": IncidentType.SECURITY_BREACH,
            "priority": IncidentPriority.HIGH,
            "status": IncidentStatus.IN_PROGRESS,
            "impact_description": "Posible compromiso de seguridad",
            "affected_systems": "Sistema de autenticación",
            "occurred_at": datetime.utcnow() - timedelta(hours=2),
            "detected_at": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "title": "Pérdida temporal de conectividad",
            "description": "Pérdida de conectividad de red por 30 minutos",
            "incident_type": IncidentType.SERVICE_DISRUPTION,
            "priority": IncidentPriority.MEDIUM,
            "status": IncidentStatus.CLOSED,
            "impact_description": "Servicios interrumpidos temporalmente",
            "affected_systems": "Red corporativa",
            "occurred_at": datetime.utcnow() - timedelta(days=10),
            "detected_at": datetime.utcnow() - timedelta(days=10, minutes=5),
            "resolved_at": datetime.utcnow() - timedelta(days=10, minutes=35),
            "closed_at": datetime.utcnow() - timedelta(days=9)
        }
    ]
    
    for incident_data in incidents_data:
        existing_incident = db.query(Incident).filter(Incident.title == incident_data["title"]).first()
        if not existing_incident:
            incident = Incident(
                title=incident_data["title"],
                description=incident_data["description"],
                incident_type=incident_data["incident_type"],
                priority=incident_data["priority"],
                status=incident_data["status"],
                impact_description=incident_data["impact_description"],
                affected_systems=incident_data["affected_systems"],
                occurred_at=incident_data["occurred_at"],
                detected_at=incident_data["detected_at"],
                resolved_at=incident_data.get("resolved_at"),
                closed_at=incident_data.get("closed_at"),
                reported_by=random.choice(users).id,
                response_time=random.randint(5, 60),  # minutos
                resolution_time=random.randint(30, 300)  # minutos
            )
            db.add(incident)
    
    db.commit()
    print("✅ Incidentes de prueba creados")

def create_non_conformities(db: Session):
    """Crear no conformidades de prueba"""
    users = db.query(User).all()
    
    nc_data = [
        {
            "title": "Documento sin aprobación",
            "description": "Se encontró un documento en uso sin la aprobación correspondiente",
            "severity": NonConformitySeverity.HIGH,
            "status": NonConformityStatus.IN_PROGRESS,
            "location": "Oficina Principal",
            "process_affected": "Gestión de Documentos",
            "detected_date": datetime.utcnow() - timedelta(days=3)
        },
        {
            "title": "Falta de capacitación en procedimientos",
            "description": "Personal no capacitado en nuevos procedimientos de seguridad",
            "severity": NonConformitySeverity.MEDIUM,
            "status": NonConformityStatus.OPEN,
            "location": "Área de Producción",
            "process_affected": "Capacitación",
            "detected_date": datetime.utcnow() - timedelta(days=1)
        },
        {
            "title": "Equipo de medición descalibrado",
            "description": "Equipo de medición crítico fuera de calibración",
            "severity": NonConformitySeverity.CRITICAL,
            "status": NonConformityStatus.CLOSED,
            "location": "Laboratorio de Calidad",
            "process_affected": "Control de Calidad",
            "detected_date": datetime.utcnow() - timedelta(days=15),
            "actual_resolution_date": datetime.utcnow() - timedelta(days=10),
            "root_cause": "Falta de programa de calibración preventiva",
            "corrective_action": "Implementar programa de calibración mensual",
            "preventive_action": "Establecer alertas automáticas de vencimiento"
        }
    ]
    
    for nc in nc_data:
        existing_nc = db.query(NonConformity).filter(NonConformity.title == nc["title"]).first()
        if not existing_nc:
            non_conformity = NonConformity(
                title=nc["title"],
                description=nc["description"],
                severity=nc["severity"],
                status=nc["status"],
                location=nc["location"],
                process_affected=nc["process_affected"],
                detected_date=nc["detected_date"],
                actual_resolution_date=nc.get("actual_resolution_date"),
                root_cause=nc.get("root_cause"),
                corrective_action=nc.get("corrective_action"),
                preventive_action=nc.get("preventive_action"),
                reported_by=random.choice(users).id
            )
            db.add(non_conformity)
    
    db.commit()
    print("✅ No conformidades de prueba creadas")

def create_audits(db: Session):
    """Crear auditorías de prueba"""
    users = db.query(User).all()
    auditors = [u for u in users if u.role in [UserRole.AUDITOR, UserRole.ADMIN]]
    
    audits_data = [
        {
            "title": "Auditoría Interna ISO 9001 - Q1 2024",
            "description": "Auditoría interna del sistema de gestión de calidad",
            "audit_type": AuditType.INTERNAL,
            "status": AuditStatus.COMPLETED,
            "scope": "Sistema de Gestión de Calidad completo",
            "objectives": "Verificar conformidad con ISO 9001:2015",
            "criteria": "ISO 9001:2015, Manual de Calidad",
            "planned_start_date": datetime.utcnow() - timedelta(days=30),
            "planned_end_date": datetime.utcnow() - timedelta(days=25),
            "actual_start_date": datetime.utcnow() - timedelta(days=30),
            "actual_end_date": datetime.utcnow() - timedelta(days=25),
            "findings_count": 3,
            "non_conformities_count": 1,
            "observations_count": 2,
            "recommendations_count": 5
        },
        {
            "title": "Auditoría de Seguimiento - No Conformidades",
            "description": "Auditoría de seguimiento para verificar cierre de no conformidades",
            "audit_type": AuditType.FOLLOW_UP,
            "status": AuditStatus.PLANNED,
            "scope": "No conformidades abiertas del Q1",
            "objectives": "Verificar efectividad de acciones correctivas",
            "criteria": "Plan de Acción Correctiva",
            "planned_start_date": datetime.utcnow() + timedelta(days=7),
            "planned_end_date": datetime.utcnow() + timedelta(days=10)
        }
    ]
    
    for audit_data in audits_data:
        existing_audit = db.query(Audit).filter(Audit.title == audit_data["title"]).first()
        if not existing_audit:
            audit = Audit(
                title=audit_data["title"],
                description=audit_data["description"],
                audit_type=audit_data["audit_type"],
                status=audit_data["status"],
                scope=audit_data["scope"],
                objectives=audit_data["objectives"],
                criteria=audit_data["criteria"],
                planned_start_date=audit_data["planned_start_date"],
                planned_end_date=audit_data["planned_end_date"],
                actual_start_date=audit_data.get("actual_start_date"),
                actual_end_date=audit_data.get("actual_end_date"),
                findings_count=audit_data.get("findings_count", 0),
                non_conformities_count=audit_data.get("non_conformities_count", 0),
                observations_count=audit_data.get("observations_count", 0),
                recommendations_count=audit_data.get("recommendations_count", 0),
                auditor_lead=random.choice(auditors).id
            )
            db.add(audit)
    
    db.commit()
    print("✅ Auditorías de prueba creadas")

def create_kpis(db: Session):
    """Crear KPIs de prueba"""
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    kpis_data = [
        {
            "name": "Tiempo de Resolución de Incidentes",
            "description": "Tiempo promedio para resolver incidentes críticos",
            "kpi_type": KPIType.PERFORMANCE,
            "measurement_unit": KPIMeasurementUnit.HOURS,
            "target_value": 4.0,
            "minimum_value": 0.0,
            "maximum_value": 8.0,
            "measurement_frequency": "daily"
        },
        {
            "name": "Cumplimiento de Auditorías",
            "description": "Porcentaje de auditorías completadas en tiempo",
            "kpi_type": KPIType.COMPLIANCE,
            "measurement_unit": KPIMeasurementUnit.PERCENTAGE,
            "target_value": 95.0,
            "minimum_value": 80.0,
            "maximum_value": 100.0,
            "measurement_frequency": "monthly"
        },
        {
            "name": "No Conformidades por Mes",
            "description": "Número de no conformidades reportadas mensualmente",
            "kpi_type": KPIType.QUALITY,
            "measurement_unit": KPIMeasurementUnit.COUNT,
            "target_value": 5.0,
            "minimum_value": 0.0,
            "maximum_value": 10.0,
            "measurement_frequency": "monthly"
        },
        {
            "name": "Disponibilidad del Sistema",
            "description": "Porcentaje de tiempo de disponibilidad del sistema",
            "kpi_type": KPIType.CONTINUITY,
            "measurement_unit": KPIMeasurementUnit.PERCENTAGE,
            "target_value": 99.9,
            "minimum_value": 95.0,
            "maximum_value": 100.0,
            "measurement_frequency": "daily"
        }
    ]
    
    for kpi_data in kpis_data:
        existing_kpi = db.query(KPI).filter(KPI.name == kpi_data["name"]).first()
        if not existing_kpi:
            kpi = KPI(
                name=kpi_data["name"],
                description=kpi_data["description"],
                kpi_type=kpi_data["kpi_type"],
                measurement_unit=kpi_data["measurement_unit"],
                target_value=kpi_data["target_value"],
                minimum_value=kpi_data["minimum_value"],
                maximum_value=kpi_data["maximum_value"],
                measurement_frequency=kpi_data["measurement_frequency"],
                owner=admin_user.id
            )
            db.add(kpi)
    
    db.commit()
    print("✅ KPIs de prueba creados")

def create_business_continuity_data(db: Session):
    """Crear datos de continuidad del negocio"""
    admin_user = db.query(User).filter(User.username == "admin").first()
    
    # Planes de continuidad
    plans_data = [
        {
            "title": "Plan de Continuidad - Centro de Datos",
            "description": "Plan de continuidad para el centro de datos principal",
            "status": PlanStatus.ACTIVE,
            "scope": "Infraestructura de TI crítica",
            "objectives": "Mantener servicios críticos durante interrupciones",
            "recovery_time_objective": 4,  # horas
            "recovery_point_objective": 1  # hora
        },
        {
            "title": "Plan de Continuidad - Operaciones",
            "description": "Plan de continuidad para operaciones de negocio",
            "status": PlanStatus.DRAFT,
            "scope": "Procesos de negocio críticos",
            "objectives": "Continuar operaciones durante crisis",
            "recovery_time_objective": 24,  # horas
            "recovery_point_objective": 4   # horas
        }
    ]
    
    for plan_data in plans_data:
        existing_plan = db.query(BusinessContinuityPlan).filter(
            BusinessContinuityPlan.title == plan_data["title"]
        ).first()
        if not existing_plan:
            plan = BusinessContinuityPlan(
                title=plan_data["title"],
                description=plan_data["description"],
                status=plan_data["status"],
                scope=plan_data["scope"],
                objectives=plan_data["objectives"],
                recovery_time_objective=plan_data["recovery_time_objective"],
                recovery_point_objective=plan_data["recovery_point_objective"],
                created_by=admin_user.id,
                owner=admin_user.id
            )
            db.add(plan)
    
    # Simulaciones de emergencia
    simulations_data = [
        {
            "title": "Simulación de Falla de Servidor",
            "description": "Simulación de falla completa del servidor principal",
            "status": SimulationStatus.COMPLETED,
            "scenario": "Falla de hardware en servidor principal",
            "objectives": "Probar procedimientos de recuperación",
            "participants": "Equipo de TI, Administradores",
            "planned_date": datetime.utcnow() - timedelta(days=20),
            "actual_date": datetime.utcnow() - timedelta(days=20),
            "duration_hours": 4,
            "success_rate": 85
        },
        {
            "title": "Simulación de Corte de Energía",
            "description": "Simulación de corte prolongado de energía",
            "status": SimulationStatus.PLANNED,
            "scenario": "Corte de energía por 8 horas",
            "objectives": "Probar sistemas de respaldo",
            "participants": "Todo el personal",
            "planned_date": datetime.utcnow() + timedelta(days=14),
            "duration_hours": 8
        }
    ]
    
    for sim_data in simulations_data:
        existing_sim = db.query(EmergencySimulation).filter(
            EmergencySimulation.title == sim_data["title"]
        ).first()
        if not existing_sim:
            simulation = EmergencySimulation(
                title=sim_data["title"],
                description=sim_data["description"],
                status=sim_data["status"],
                scenario=sim_data["scenario"],
                objectives=sim_data["objectives"],
                participants=sim_data["participants"],
                planned_date=sim_data["planned_date"],
                actual_date=sim_data.get("actual_date"),
                duration_hours=sim_data["duration_hours"],
                success_rate=sim_data.get("success_rate"),
                created_by=admin_user.id,
                coordinator=admin_user.id
            )
            db.add(simulation)
    
    db.commit()
    print("✅ Datos de continuidad del negocio creados")

def main():
    """Función principal para inicializar datos"""
    print("🚀 Inicializando datos de prueba para SGCN-SGC Prototype...")
    
    # Crear tablas
    create_tables()
    
    # Crear datos de prueba
    db = SessionLocal()
    try:
        create_users(db)
        create_documents(db)
        create_incidents(db)
        create_non_conformities(db)
        create_audits(db)
        create_kpis(db)
        create_business_continuity_data(db)
        
        print("\n✅ ¡Datos de prueba inicializados correctamente!")
        print("\n📋 Usuarios de prueba creados:")
        print("   • admin / admin (Administrador)")
        print("   • auditor1 / auditor (Auditor)")
        print("   • gestor1 / gestor (Gestor)")
        print("   • operador1 / operador (Operador)")
        print("\n🌐 Accede a la aplicación en: http://localhost:8000")
        print("📚 Documentación API en: http://localhost:8000/docs")
        
    except Exception as e:
        print(f"❌ Error al inicializar datos: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
