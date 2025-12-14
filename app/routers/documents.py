"""
Router para gestión de documentos (RF-01)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas import DocumentCreate, DocumentUpdate, Document as DocumentSchema, MessageResponse
from app.auth import get_current_active_user, require_role
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/documents", tags=["documents"])

# Directorio para almacenar documentos
UPLOAD_DIR = "uploads/documents"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=DocumentSchema)
def create_document(
    document: DocumentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo documento"""
    db_document = Document(
        title=document.title,
        description=document.description,
        document_type=document.document_type,
        version=document.version,
        status=document.status,
        created_by=current_user.id
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@router.get("/", response_model=List[DocumentSchema])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener lista de documentos"""
    documents = db.query(Document).offset(skip).limit(limit).all()
    return documents

@router.get("/{document_id}", response_model=DocumentSchema)
def get_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener documento por ID"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.put("/{document_id}", response_model=DocumentSchema)
def update_document(
    document_id: int,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar documento"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Solo el creador o admin puede editar
    if document.created_by != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = document_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)
    
    document.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(document)
    
    return document

@router.delete("/{document_id}", response_model=MessageResponse)
def delete_document(
    document_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Eliminar documento (solo admin)"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Eliminar archivo si existe
    if document.file_path and os.path.exists(document.file_path):
        os.remove(document.file_path)
    
    db.delete(document)
    db.commit()
    
    return MessageResponse(message="Document deleted successfully")

@router.post("/{document_id}/upload")
def upload_document_file(
    document_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Subir archivo para un documento"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Generar nombre único para el archivo
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Guardar archivo
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Actualizar documento
    document.file_path = file_path
    document.file_size = len(content)
    document.mime_type = file.content_type
    document.updated_at = datetime.utcnow()
    
    db.commit()
    
    return MessageResponse(message="File uploaded successfully")

@router.post("/{document_id}/approve", response_model=DocumentSchema)
def approve_document(
    document_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Aprobar documento (solo admin)"""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document.status = "approved"
    document.approved_by = current_user.id
    document.approved_at = datetime.utcnow()
    document.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(document)
    
    return document

