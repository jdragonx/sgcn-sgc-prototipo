# SGCN-SGC Prototypo

Sistema Integrado de Gestión de Calidad y Continuidad del Negocio - Prototipo

## Descripción

Este es un prototipo del sistema SGCN-SGC que implementa los requisitos funcionales para la gestión integrada de calidad (ISO 9001) y continuidad del negocio (ISO 22301).

## Características Principales

### Módulos Implementados

1. **Gestión de Documentos (RF-01)**
   - Carga, revisión y aprobación de manuales, políticas y procedimientos
   - Control de versiones
   - Estados: draft, pending_review, approved, rejected, obsolete

2. **Registro de No Conformidades (RF-02)**
   - Anotación y seguimiento de problemas
   - Análisis de causa raíz
   - Acciones correctivas y preventivas
   - Estados: open, in_progress, closed, cancelled

3. **Gestión de Incidentes (RF-03)**
   - Registro de eventos críticos
   - Clasificación por prioridad y tipo
   - Seguimiento hasta resolución
   - Estados: open, in_progress, resolved, closed, cancelled

4. **Simulaciones de Emergencia (RF-04)**
   - Programación de simulacros
   - Evaluación de resultados
   - Lecciones aprendidas

5. **Planes de Continuidad (RF-05)**
   - Creación y gestión de planes BCP
   - Objetivos RTO/RPO
   - Estados: draft, active, tested, obsolete

6. **Auditorías Internas (RF-06)**
   - Programación de auditorías
   - Documentación de hallazgos
   - Estados: planned, in_progress, completed, cancelled

7. **Control de Cambios (RF-07)**
   - Registro de cambios importantes
   - Análisis de impacto
   - Planes de implementación

8. **Indicadores de Desempeño (RF-08)**
   - KPIs de calidad y continuidad
   - Mediciones y tendencias
   - Dashboards ejecutivos

9. **Usuarios y Permisos (RF-09)**
   - Roles: admin, auditor, gestor, operador
   - Autenticación JWT
   - Control de acceso

10. **Notificaciones y Alertas (RF-10)**
    - Sistema de alertas multicanal
    - Escalamiento automático
    - Operación offline

## Tecnologías Utilizadas

- **Backend**: FastAPI (Python)
- **Base de Datos**: SQLite (prototipo)
- **Autenticación**: JWT con Passlib
- **ORM**: SQLAlchemy
- **Validación**: Pydantic
- **Gestión de Dependencias**: uv

## Instalación y Configuración

### Prerrequisitos

- Python 3.11+
- uv (gestor de paquetes)

### Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd sgcn-sgc-prototype
```

2. Instalar dependencias:
```bash
uv sync
```

3. Configurar variables de entorno:
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

4. Ejecutar la aplicación:
```bash
uv run python -m app.main
```

La aplicación estará disponible en `http://localhost:8000`

## Uso de la API

### Autenticación

1. Registrar un usuario:
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Administrador",
    "password": "password123",
    "role": "admin"
  }'
```

2. Iniciar sesión:
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password123"
```

### Endpoints Principales

- **Documentación API**: `GET /docs`
- **Dashboard**: `GET /dashboard/stats`
- **Documentos**: `GET /documents/`
- **Incidentes**: `GET /incidents/`
- **No Conformidades**: `GET /non-conformities/`
- **Auditorías**: `GET /audits/`
- **KPIs**: `GET /kpis/`

## Estructura del Proyecto

```
sgcn-sgc-prototype/
├── app/
│   ├── models/          # Modelos de base de datos
│   ├── routers/         # Endpoints de la API
│   ├── static/          # Archivos estáticos
│   ├── templates/       # Plantillas HTML
│   ├── auth.py          # Autenticación
│   ├── main.py          # Aplicación principal
│   └── schemas.py       # Esquemas Pydantic
├── uploads/             # Archivos subidos
├── pyproject.toml       # Configuración del proyecto
└── README.md           # Este archivo
```

## Características del Prototipo

- **Simplicidad**: Diseñado para ser lo más simple posible
- **Mocks**: Algunas funcionalidades usan datos simulados
- **Base de datos**: SQLite para facilitar el desarrollo
- **Autenticación**: Sistema básico de usuarios y roles
- **API REST**: Endpoints completos para todas las funcionalidades
- **Documentación**: API auto-documentada con Swagger

## Próximos Pasos

Para convertir este prototipo en un sistema de producción:

1. **Base de Datos**: Migrar a PostgreSQL o MySQL
2. **Frontend**: Desarrollar interfaz web completa
3. **Notificaciones**: Implementar sistema real de email/SMS
4. **Seguridad**: Mejorar autenticación y autorización
5. **Testing**: Agregar tests unitarios e integración
6. **Deployment**: Configurar para producción
7. **Monitoreo**: Agregar logging y métricas

## Contribución

Este es un prototipo desarrollado para demostrar las capacidades del sistema SGCN-SGC. Para contribuir o reportar problemas, por favor contacta al equipo de desarrollo.

## Licencia

Este proyecto es un prototipo interno y está sujeto a las políticas de la organización.

