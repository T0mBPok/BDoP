from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import ForeignKey
from src.database import int_pk, str_null_true, Base, str_uniq
from src.tasks.models import Task
from datetime import datetime
from src.users.models import User
from src.associations import project_users
from src.categories.models import Category
    

class Project(Base):
    id: Mapped[int_pk]
    name: Mapped[str]
    description: Mapped[str_null_true]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime]
    tasks: Mapped["Task"] = relationship("Task", back_populates="project")
    image_id: Mapped[int] = mapped_column(ForeignKey('project_images.id', ondelete="CASCADE"), nullable=True)
    
    project_image: Mapped['ProjectImage'] = relationship("ProjectImage", uselist=False, foreign_keys=[image_id], 
                                                        cascade="all, delete-orphan",
                                                        single_parent=True,
                                                        back_populates="project",
                                                        passive_deletes=True)
    category: Mapped["Category"] = relationship("Category")
    author: Mapped['User'] = relationship("User", back_populates="authored_projects")
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary = project_users,
        back_populates = 'projects'
    )

class ProjectImage(Base):
    __tablename__ = 'project_images'
    id: Mapped[int_pk]
    filepath: Mapped[str_uniq]
    project = relationship("Project", back_populates="project_image", uselist=False)