from src.database import Base, str_uniq, int_pk, str_null_true
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from datetime import date
from src.categories.models import Category
from src.users.models import User
from src.projects.models import Project

class Subtit(Base):
    __tablename__ = 'substacles'
    
    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    performer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    description: Mapped[str_null_true]
    created_at: Mapped[date]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    deadline: Mapped[date]
    importance_color: Mapped[int]
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    is_completed: Mapped[bool]
    
    category: Mapped["Category"] = relationship("Category")
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    performer: Mapped["User"] = relationship("User", foreign_keys=[performer_id])
    task: Mapped["Task"] = relationship("Task")
    project: Mapped["Project"] = relationship("Project")
    