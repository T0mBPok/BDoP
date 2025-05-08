from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from src.database import int_pk, str_null_true, Base
from src.tasks.models import Task
from datetime import datetime
from src.users.models import User
from src.associations import project_users
    

class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    category_color: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime]
    tasks: Mapped["Task"] = relationship("Task", back_populates="project")
    
    author: Mapped['User'] = relationship("User", back_populates="authored_projects")
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary = project_users,
        back_populates = 'projects'
    )