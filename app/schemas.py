"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums para los esquemas
class UserRole(str, Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    GESTOR = "gestor"
    OPERADOR = "operador"

class DocumentStatus(str, Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    OBSOLETE = "obsolete"

class DocumentType(str, Enum):
    MANUAL = "manual"
    POLICY = "policy"
    PROCEDURE = "procedure"
    FORM = "form"
    RECORD = "record"

# Esquemas de Usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.OPERADOR

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de Documento
class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None
    document_type: DocumentType
    version: str = "1.0"
    status: DocumentStatus = DocumentStatus.DRAFT

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    document_type: Optional[DocumentType] = None
    version: Optional[str] = None
    status: Optional[DocumentStatus] = None

class Document(DocumentBase):
    id: int
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    effective_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de No Conformidad
class NonConformitySeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class NonConformityStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class NonConformityBase(BaseModel):
    title: str
    description: str
    severity: NonConformitySeverity
    location: Optional[str] = None
    process_affected: Optional[str] = None
    detected_date: datetime

class NonConformityCreate(NonConformityBase):
    pass

class NonConformityUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[NonConformitySeverity] = None
    status: Optional[NonConformityStatus] = None
    location: Optional[str] = None
    process_affected: Optional[str] = None
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None

class NonConformity(NonConformityBase):
    id: int
    status: NonConformityStatus
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    preventive_action: Optional[str] = None
    target_resolution_date: Optional[datetime] = None
    actual_resolution_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de Incidente
class IncidentPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class IncidentType(str, Enum):
    SYSTEM_FAILURE = "system_failure"
    SECURITY_BREACH = "security_breach"
    DATA_LOSS = "data_loss"
    SERVICE_DISRUPTION = "service_disruption"
    OTHER = "other"

class IncidentBase(BaseModel):
    title: str
    description: str
    incident_type: IncidentType
    priority: IncidentPriority
    impact_description: Optional[str] = None
    affected_systems: Optional[str] = None
    occurred_at: datetime
    detected_at: datetime

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    incident_type: Optional[IncidentType] = None
    priority: Optional[IncidentPriority] = None
    status: Optional[IncidentStatus] = None
    impact_description: Optional[str] = None
    affected_systems: Optional[str] = None
    business_impact: Optional[str] = None
    resolution_steps: Optional[str] = None
    lessons_learned: Optional[str] = None

class Incident(IncidentBase):
    id: int
    status: IncidentStatus
    business_impact: Optional[str] = None
    resolution_steps: Optional[str] = None
    lessons_learned: Optional[str] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    response_time: Optional[int] = None
    resolution_time: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de Auditoría
class AuditStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class AuditType(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    FOLLOW_UP = "follow_up"
    SPECIAL = "special"

class AuditBase(BaseModel):
    title: str
    description: Optional[str] = None
    audit_type: AuditType
    scope: Optional[str] = None
    objectives: Optional[str] = None
    criteria: Optional[str] = None
    planned_start_date: Optional[datetime] = None
    planned_end_date: Optional[datetime] = None

class AuditCreate(AuditBase):
    pass

class AuditUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    audit_type: Optional[AuditType] = None
    status: Optional[AuditStatus] = None
    scope: Optional[str] = None
    objectives: Optional[str] = None
    criteria: Optional[str] = None

class Audit(AuditBase):
    id: int
    status: AuditStatus
    actual_start_date: Optional[datetime] = None
    actual_end_date: Optional[datetime] = None
    findings_count: int = 0
    non_conformities_count: int = 0
    observations_count: int = 0
    recommendations_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas de KPI
class KPIType(str, Enum):
    QUALITY = "quality"
    CONTINUITY = "continuity"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    CUSTOMER = "customer"

class KPIMeasurementUnit(str, Enum):
    PERCENTAGE = "percentage"
    COUNT = "count"
    HOURS = "hours"
    DAYS = "days"
    CURRENCY = "currency"
    RATIO = "ratio"

class KPIBase(BaseModel):
    name: str
    description: Optional[str] = None
    kpi_type: KPIType
    measurement_unit: KPIMeasurementUnit
    target_value: Optional[float] = None
    minimum_value: Optional[float] = None
    maximum_value: Optional[float] = None
    measurement_frequency: str = "monthly"

class KPICreate(KPIBase):
    pass

class KPIUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    kpi_type: Optional[KPIType] = None
    measurement_unit: Optional[KPIMeasurementUnit] = None
    target_value: Optional[float] = None
    minimum_value: Optional[float] = None
    maximum_value: Optional[float] = None
    measurement_frequency: Optional[str] = None

class KPI(KPIBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class KPIMeasurementBase(BaseModel):
    measured_value: float
    measurement_date: datetime
    notes: Optional[str] = None
    data_source: Optional[str] = None

class KPIMeasurementCreate(KPIMeasurementBase):
    kpi_id: int

class KPIMeasurement(KPIMeasurementBase):
    id: int
    kpi_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Esquemas de respuesta
class MessageResponse(BaseModel):
    message: str
    success: bool = True

class DashboardStats(BaseModel):
    total_documents: int
    pending_documents: int
    total_incidents: int
    open_incidents: int
    total_non_conformities: int
    open_non_conformities: int
    total_audits: int
    planned_audits: int
    total_kpis: int
    recent_activities: List[dict] = []

