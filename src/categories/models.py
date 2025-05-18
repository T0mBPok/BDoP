from src.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.users.models import User

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int_pk]
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    name: Mapped[str_uniq]
    color: Mapped[str]
    
    user: Mapped["User"] = relationship("User")   
        