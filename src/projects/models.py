from sqlalchemy import select, func
from sqlalchemy.orm import Mapped, column_property, relationship
from src.database import int_pk, str_null_true, Base
from src.tasks.models import Task
from datetime import datetime
    

class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    category_color: Mapped[int]
    created_at: Mapped[datetime]
    # tasks_count: Mapped[int] = column_property
    tasks: Mapped["Task"] = relationship("Task", back_populates="projects")
    
# tasks_count = column_property(
#     select(func.count(Task.id))
#     .where(Task.project_id == Project.id)
#     .correlate_except(Task)
#     .scalar_subquery()
# )