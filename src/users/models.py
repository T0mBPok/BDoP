from src.database import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[str_uniq]
    email: Mapped[str_uniq]
    password: Mapped[str]
    
    is_user: Mapped[bool] = mapped_column(default=True, server_default = text('true'))
    is_admin: Mapped[bool] = mapped_column(default = False, server_default = text('false'))
    
    extend_existing = True
    
    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id})"