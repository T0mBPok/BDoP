from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, int_pk, str_null_true
from src.categories.models import Category


class Task(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    performer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    description: Mapped[str_null_true]
    created_at: Mapped[date]
    deadline: Mapped[date]
    importance_color: Mapped[int]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    is_completed: Mapped[bool]
    
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")
    performer = relationship("User", back_populates="attached_tasks", foreign_keys=[performer_id])
    author = relationship("User", back_populates="authored_tasks", foreign_keys=[author_id])
    category: Mapped["Category"] = relationship("Category")