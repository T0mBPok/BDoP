from src.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, text
from src.associations import project_users

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default = False, server_default = text('false'))
    image_id: Mapped[int] = mapped_column(ForeignKey('images.id', ondelete="CASCADE"), nullable=True)
    
    image: Mapped['Image'] = relationship("Image", uselist=False)
    authored_projects: Mapped[list["Project"]] = relationship("Project", back_populates="author")
    projects :Mapped[list["Project"]] = relationship(
        "Project",
        secondary = project_users,
        back_populates='users'
    )
    attached_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="performer",
        foreign_keys="[Task.performer_id, Subtit.performer_id]"
    )
    authored_tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="author",
        foreign_keys="[Task.author_id, Subtit.author_id]",
        cascade="all, delete-orphan"
    )
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"
    
class Image(Base):
    id: Mapped[int_pk]
    filepath: Mapped[str_uniq]
    user = relationship("User", back_populates="image", uselist=False)