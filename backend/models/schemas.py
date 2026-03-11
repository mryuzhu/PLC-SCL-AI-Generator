from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

ModeType = Literal["safe", "balanced", "free"]


class ProjectCreate(BaseModel):
    name: str = Field(min_length=2, max_length=128)


class ProjectOut(BaseModel):
    id: int
    name: str
    created_at: datetime

    class Config:
        from_attributes = True


class TaskCreate(BaseModel):
    project_id: int
    prompt: str = Field(min_length=5)
    mode: ModeType = "balanced"
    template: str | None = None


class TaskOut(BaseModel):
    id: int
    project_id: int
    prompt: str
    mode: str
    status: str

    class Config:
        from_attributes = True


class GenerateRequest(BaseModel):
    prompt: str
    mode: ModeType = "balanced"
    model: str = "local"
    template: str | None = None


class ValidationIssue(BaseModel):
    code: str
    message: str


class ValidationResult(BaseModel):
    status: Literal["pass", "warning", "error"]
    warnings: list[ValidationIssue] = []
    errors: list[ValidationIssue] = []


class GenerateResponse(BaseModel):
    scl_code: str
    validation: ValidationResult


class ValidateRequest(BaseModel):
    scl_code: str
    mode: ModeType = "balanced"


class TIAImportRequest(BaseModel):
    project_path: str
    scl_file: str


class TIAImportResponse(BaseModel):
    status: str
    message: str
