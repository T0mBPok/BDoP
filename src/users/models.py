from src.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from src.associations import project_users
from src.images.models import Image

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default = False, server_default = text('false'))
    image_id: Mapped[int] = mapped_column(ForeignKey('images.id'), nullable=True)
    
    image: Mapped['Image'] = relationship("Image",
                                        uselist=False,
                                        back_populates="user",
                                        cascade="all, delete-orphan",
                                        single_parent=True,
                                        passive_deletes=True)
    authored_projects: Mapped[list["Project"]] = relationship("Project", back_populates="author")
    projects :Mapped[list["Project"]] = relationship(
        "Project",
        secondary = project_users,
        back_populates='users'
    )
    attached_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="performer",
        foreign_keys="[Task.performer_id]"
    )
    attached_substacles: Mapped[list["Subtit"]] = relationship(
        "Subtit",
        back_populates="performer",
        foreign_keys="[Subtit.performer_id]"
    )
    authored_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="author",
        foreign_keys="[Task.author_id, Subtit.author_id]",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"