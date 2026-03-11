from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.core.scl_generator.generator import SCLGenerator
from backend.core.tia_integration.service import TIAIntegrationService
from backend.core.validator.validator import CodeValidator
from backend.models.database import get_db
from backend.models.entities import Code, Project, Task
from backend.models.schemas import (
    GenerateRequest,
    GenerateResponse,
    ProjectCreate,
    ProjectOut,
    TaskCreate,
    TaskOut,
    TIAImportRequest,
    TIAImportResponse,
    ValidateRequest,
    ValidationResult,
)
from backend.services.task_manager import TaskManager

router = APIRouter()

generator = SCLGenerator()
validator = CodeValidator()
task_manager = TaskManager()
tia_service = TIAIntegrationService()


@router.post("/projects", response_model=ProjectOut)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)):
    project = Project(name=payload.name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects", response_model=list[ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(Project).order_by(Project.created_at.desc()).all()


@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"status": "deleted"}


@router.post("/task/create", response_model=TaskOut)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    if not db.get(Project, payload.project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    task = task_manager.create_and_run(
        db=db,
        project_id=payload.project_id,
        prompt=payload.prompt,
        mode=payload.mode,
        model="local",
        template=payload.template,
    )
    return task


@router.get("/task/status/{task_id}", response_model=TaskOut)
def get_task_status(task_id: int, db: Session = Depends(get_db)):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/task/result/{task_id}")
def get_task_result(task_id: int, db: Session = Depends(get_db)):
    code = db.get(Code, task_id)
    if not code:
        raise HTTPException(status_code=404, detail="Task result not found")
    return {"task_id": task_id, "scl_code": code.scl_code, "validation": code.validation_result}


@router.post("/generate", response_model=GenerateResponse)
def generate(payload: GenerateRequest):
    scl_code = generator.generate(payload.prompt, mode=payload.mode, model=payload.model, template=payload.template)
    validation = validator.validate(scl_code, mode=payload.mode)
    return GenerateResponse(scl_code=scl_code, validation=validation)


@router.post("/validate", response_model=ValidationResult)
def validate(payload: ValidateRequest):
    return validator.validate(payload.scl_code, mode=payload.mode)


@router.post("/tia/import", response_model=TIAImportResponse)
def tia_import(payload: TIAImportRequest):
    status, message = tia_service.import_to_tia(payload.project_path, payload.scl_file)
    return TIAImportResponse(status=status, message=message)
