"""
Modelo de Documento para gestión de documentos (RF-01)
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.database import Base
import enum

class DocumentStatus(str, enum.Enum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    OBSOLETE = "obsolete"

class DocumentType(str, enum.Enum):
    MANUAL = "manual"
    POLICY = "policy"
    PROCEDURE = "procedure"
    FORM = "form"
    RECORD = "record"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    document_type = Column(Enum(DocumentType), nullable=False)
    version = Column(String(20), default="1.0")
    status = Column(Enum(DocumentStatus), default=DocumentStatus.DRAFT)
    file_path = Column(String(500))  # Ruta al archivo en el sistema
    file_size = Column(Integer)  # Tamaño en bytes
    mime_type = Column(String(100))
    
    # Relaciones
    created_by = Column(Integer, ForeignKey("users.id"))
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    approved_by = Column(Integer, ForeignKey("users.id"))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    reviewed_at = Column(DateTime(timezone=True))
    approved_at = Column(DateTime(timezone=True))
    effective_date = Column(DateTime(timezone=True))
    expiry_date = Column(DateTime(timezone=True))
    
    # Relaciones
    creator = relationship("User", foreign_keys=[created_by])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    approver = relationship("User", foreign_keys=[approved_by])
    
    def __repr__(self):
        return f"<Document(title='{self.title}', version='{self.version}', status='{self.status}')>"

