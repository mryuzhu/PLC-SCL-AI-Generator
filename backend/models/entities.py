from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tasks: Mapped[list["Task"]] = relationship(back_populates="project", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    prompt: Mapped[str] = mapped_column(Text)
    mode: Mapped[str] = mapped_column(String(32), default="balanced")
    status: Mapped[str] = mapped_column(String(32), default="pending")
    result: Mapped[str] = mapped_column(Text, default="")

    project: Mapped[Project] = relationship(back_populates="tasks")
    code: Mapped["Code"] = relationship(back_populates="task", uselist=False, cascade="all, delete-orphan")


class Code(Base):
    __tablename__ = "codes"

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"), primary_key=True)
    scl_code: Mapped[str] = mapped_column(Text)
    validation_result: Mapped[str] = mapped_column(Text)

    task: Mapped[Task] = relationship(back_populates="code")
