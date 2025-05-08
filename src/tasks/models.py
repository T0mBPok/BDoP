from datetime import datetime, date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, int_pk, str_null_true


class Task(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    category_color: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    performer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    description: Mapped[str_null_true]
    created_at: Mapped[datetime]
    deadline: Mapped[date]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    performer = relationship("User", back_populates="attached_tasks", foreign_keys=[performer_id])
    author = relationship("User", back_populates="authored_tasks", foreign_keys=[author_id])