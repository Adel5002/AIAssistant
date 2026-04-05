from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database.models.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32))
    
    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")