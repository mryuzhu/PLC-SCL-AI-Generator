from sqlalchemy.orm import Session

from backend.core.scl_generator.generator import SCLGenerator
from backend.core.validator.validator import CodeValidator
from backend.models.entities import Code, Task


class TaskManager:
    def __init__(self) -> None:
        self.generator = SCLGenerator()
        self.validator = CodeValidator()

    def create_and_run(self, db: Session, project_id: int, prompt: str, mode: str, model: str, template: str | None = None) -> Task:
        task = Task(project_id=project_id, prompt=prompt, mode=mode, status="running", result="")
        db.add(task)
        db.flush()

        scl_code = self.generator.generate(requirement=prompt, mode=mode, model=model, template=template)
        validation = self.validator.validate(scl_code=scl_code, mode=mode)

        task.status = "done" if validation.status != "error" else "failed"
        task.result = validation.model_dump_json()

        db.merge(Code(task_id=task.id, scl_code=scl_code, validation_result=validation.model_dump_json()))
        db.commit()
        db.refresh(task)
        return task
