from datetime import date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base, int_pk, str_null_true


class Task(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    category_color: Mapped[str]
    importance_color: Mapped[str]
    perfomer: Mapped[str_null_true] 
    author: Mapped[str]
    description: Mapped[str_null_true]
    created_at: Mapped[date]
    deadline: Mapped[date]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    
    project: Mapped["Project"] = relationship("Project", back_populates='tasks')