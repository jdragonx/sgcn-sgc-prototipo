"""
Aplicación principal del sistema SGCN-SGC
"""
from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models.database import engine, Base
from app.routers import auth, documents, incidents, non_conformities, audits, kpis, dashboard, notifications, business_continuity as bc_router
from app.models import user, document, non_conformity, incident, audit, business_continuity, notification, kpi, change_control
import os

# Crear las tablas de la base de datos
Base.metadata.create_all(bind=engine)

# Crear directorio de uploads
os.makedirs("uploads/documents", exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="SGCN-SGC Prototype",
    description="Sistema Integrado de Gestión de Calidad y Continuidad del Negocio - Prototipo",
    version="1.0.0"
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

# Incluir routers con prefijo /api
app.include_router(auth.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(incidents.router, prefix="/api")
app.include_router(non_conformities.router, prefix="/api")
app.include_router(audits.router, prefix="/api")
app.include_router(kpis.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(notifications.router, prefix="/api")
app.include_router(bc_router.router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Página principal del sistema"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health_check():
    """Verificación de salud del sistema"""
    return {
        "status": "healthy",
        "message": "SGCN-SGC Prototype is running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
