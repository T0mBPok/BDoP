from sqlalchemy import select, func
from sqlalchemy.orm import Mapped, column_property
from src.database import int_pk, str_null_true, Base
from src.tasks.models import Task
    

class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    category_color: Mapped[str]
    tasks_count: Mapped[int] = column_property
    
    tasks_count = column_property(   
        select(func.count(Task.id))
        .where(Task.project_id == id)
        .correlate_except(Task)
        .scalar_subquery()
    )