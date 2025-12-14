"""
Router para continuidad del negocio (RF-04, RF-05)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User
from app.models.business_continuity import BusinessContinuityPlan, EmergencySimulation
from app.schemas import MessageResponse
from app.auth import get_current_active_user, require_role
from datetime import datetime
from pydantic import BaseModel

router = APIRouter(prefix="/business-continuity", tags=["business-continuity"])

# Esquemas para continuidad del negocio
class BusinessContinuityPlanBase(BaseModel):
    title: str
    description: str = None
    scope: str = None
    objectives: str = None
    recovery_time_objective: int = None  # RTO en horas
    recovery_point_objective: int = None  # RPO en horas

class BusinessContinuityPlanCreate(BusinessContinuityPlanBase):
    pass

class BusinessContinuityPlanUpdate(BaseModel):
    title: str = None
    description: str = None
    scope: str = None
    objectives: str = None
    recovery_time_objective: int = None
    recovery_point_objective: int = None
    status: str = None

class EmergencySimulationBase(BaseModel):
    title: str
    description: str = None
    scenario: str = None
    objectives: str = None
    participants: str = None
    planned_date: datetime = None
    duration_hours: int = None

class EmergencySimulationCreate(EmergencySimulationBase):
    pass

class EmergencySimulationUpdate(BaseModel):
    title: str = None
    description: str = None
    scenario: str = None
    objectives: str = None
    participants: str = None
    planned_date: datetime = None
    duration_hours: int = None
    status: str = None

# Rutas para Planes de Continuidad
@router.post("/plans/", response_model=dict)
def create_business_continuity_plan(
    plan: BusinessContinuityPlanCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nuevo plan de continuidad del negocio"""
    db_plan = BusinessContinuityPlan(
        title=plan.title,
        description=plan.description,
        scope=plan.scope,
        objectives=plan.objectives,
        recovery_time_objective=plan.recovery_time_objective,
        recovery_point_objective=plan.recovery_point_objective,
        created_by=current_user.id,
        owner=current_user.id
    )
    
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    
    return {
        "id": db_plan.id,
        "title": db_plan.title,
        "description": db_plan.description,
        "status": db_plan.status,
        "created_at": db_plan.created_at.isoformat()
    }

@router.get("/plans/", response_model=List[dict])
def get_business_continuity_plans(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener planes de continuidad del negocio"""
    plans = db.query(BusinessContinuityPlan).offset(skip).limit(limit).all()
    
    return [
        {
            "id": plan.id,
            "title": plan.title,
            "description": plan.description,
            "status": plan.status,
            "rto_hours": plan.recovery_time_objective,
            "rpo_hours": plan.recovery_point_objective,
            "created_at": plan.created_at.isoformat(),
            "last_tested": plan.last_tested.isoformat() if plan.last_tested else None
        } for plan in plans
    ]

@router.get("/plans/{plan_id}", response_model=dict)
def get_business_continuity_plan(
    plan_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener plan de continuidad por ID"""
    plan = db.query(BusinessContinuityPlan).filter(BusinessContinuityPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Business continuity plan not found")
    
    return {
        "id": plan.id,
        "title": plan.title,
        "description": plan.description,
        "scope": plan.scope,
        "objectives": plan.objectives,
        "status": plan.status,
        "rto_hours": plan.recovery_time_objective,
        "rpo_hours": plan.recovery_point_objective,
        "created_at": plan.created_at.isoformat(),
        "updated_at": plan.updated_at.isoformat() if plan.updated_at else None,
        "last_tested": plan.last_tested.isoformat() if plan.last_tested else None,
        "next_review": plan.next_review.isoformat() if plan.next_review else None
    }

@router.put("/plans/{plan_id}", response_model=dict)
def update_business_continuity_plan(
    plan_id: int,
    plan_update: BusinessContinuityPlanUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Actualizar plan de continuidad del negocio"""
    plan = db.query(BusinessContinuityPlan).filter(BusinessContinuityPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Business continuity plan not found")
    
    # Solo el propietario o admin puede editar
    can_edit = (
        plan.owner == current_user.id or
        current_user.role.value == "admin"
    )
    
    if not can_edit:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    update_data = plan_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(plan, field, value)
    
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)
    
    return {
        "id": plan.id,
        "title": plan.title,
        "status": plan.status,
        "updated_at": plan.updated_at.isoformat()
    }

# Rutas para Simulaciones de Emergencia
@router.post("/simulations/", response_model=dict)
def create_emergency_simulation(
    simulation: EmergencySimulationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Crear nueva simulación de emergencia"""
    db_simulation = EmergencySimulation(
        title=simulation.title,
        description=simulation.description,
        scenario=simulation.scenario,
        objectives=simulation.objectives,
        participants=simulation.participants,
        planned_date=simulation.planned_date,
        duration_hours=simulation.duration_hours,
        created_by=current_user.id,
        coordinator=current_user.id
    )
    
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    
    return {
        "id": db_simulation.id,
        "title": db_simulation.title,
        "description": db_simulation.description,
        "status": db_simulation.status,
        "planned_date": db_simulation.planned_date.isoformat() if db_simulation.planned_date else None,
        "created_at": db_simulation.created_at.isoformat()
    }

@router.get("/simulations/", response_model=List[dict])
def get_emergency_simulations(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener simulaciones de emergencia"""
    query = db.query(EmergencySimulation)
    
    if status_filter:
        query = query.filter(EmergencySimulation.status == status_filter)
    
    simulations = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": sim.id,
            "title": sim.title,
            "description": sim.description,
            "status": sim.status,
            "scenario": sim.scenario,
            "planned_date": sim.planned_date.isoformat() if sim.planned_date else None,
            "actual_date": sim.actual_date.isoformat() if sim.actual_date else None,
            "duration_hours": sim.duration_hours,
            "success_rate": sim.success_rate,
            "created_at": sim.created_at.isoformat()
        } for sim in simulations
    ]

@router.post("/simulations/{simulation_id}/start", response_model=dict)
def start_emergency_simulation(
    simulation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Iniciar simulación de emergencia"""
    simulation = db.query(EmergencySimulation).filter(EmergencySimulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Emergency simulation not found")
    
    if simulation.status != "planned":
        raise HTTPException(status_code=400, detail="Simulation must be in planned status to start")
    
    simulation.status = "in_progress"
    simulation.actual_date = datetime.utcnow()
    simulation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(simulation)
    
    return {
        "id": simulation.id,
        "title": simulation.title,
        "status": simulation.status,
        "actual_date": simulation.actual_date.isoformat()
    }

@router.post("/simulations/{simulation_id}/complete", response_model=dict)
def complete_emergency_simulation(
    simulation_id: int,
    success_rate: int,
    lessons_learned: str = None,
    improvement_actions: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Completar simulación de emergencia"""
    simulation = db.query(EmergencySimulation).filter(EmergencySimulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Emergency simulation not found")
    
    if simulation.status != "in_progress":
        raise HTTPException(status_code=400, detail="Simulation must be in progress to complete")
    
    simulation.status = "completed"
    simulation.success_rate = success_rate
    simulation.lessons_learned = lessons_learned
    simulation.improvement_actions = improvement_actions
    simulation.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(simulation)
    
    return {
        "id": simulation.id,
        "title": simulation.title,
        "status": simulation.status,
        "success_rate": simulation.success_rate,
        "completed_at": simulation.updated_at.isoformat()
    }

@router.get("/stats/summary")
def get_business_continuity_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de continuidad del negocio"""
    # Planes de continuidad
    total_plans = db.query(BusinessContinuityPlan).count()
    active_plans = db.query(BusinessContinuityPlan).filter(BusinessContinuityPlan.status == "active").count()
    tested_plans = db.query(BusinessContinuityPlan).filter(BusinessContinuityPlan.status == "tested").count()
    
    # Simulaciones
    total_simulations = db.query(EmergencySimulation).count()
    planned_simulations = db.query(EmergencySimulation).filter(EmergencySimulation.status == "planned").count()
    completed_simulations = db.query(EmergencySimulation).filter(EmergencySimulation.status == "completed").count()
    
    # Promedio de éxito de simulaciones
    completed_sims = db.query(EmergencySimulation).filter(EmergencySimulation.status == "completed").all()
    avg_success_rate = sum(sim.success_rate for sim in completed_sims) / len(completed_sims) if completed_sims else 0
    
    return {
        "plans": {
            "total": total_plans,
            "active": active_plans,
            "tested": tested_plans
        },
        "simulations": {
            "total": total_simulations,
            "planned": planned_simulations,
            "completed": completed_simulations,
            "average_success_rate": round(avg_success_rate, 2)
        }
    }

