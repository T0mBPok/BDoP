from sqlalchemy.orm import Mapped, relationship
from src.database import str_uniq, int_pk, Base

class Image(Base):
    id: Mapped[int_pk]
    filepath: Mapped[str_uniq]
    author_id: Mapped[int]
    user = relationship("User", back_populates="image", uselist=False)
    project = relationship("Project", back_populates='image', uselist=False, primaryjoin="Image.id == Project.image_id")