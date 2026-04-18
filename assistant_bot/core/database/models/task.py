import enum
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, String, Integer, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database.models.base import Base

def get_default_reminder():
    return datetime.now(timezone.utc).replace(hour=18, minute=0, second=0, microsecond=0)

class TaskType(enum.Enum):
    normal = "normal"
    interval = "interval"

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column()
    
    interval_seconds: Mapped[int] = mapped_column(Integer, default=3600)
    last_reminded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=get_default_reminder
    )
    date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    type: Mapped[TaskType] = mapped_column(Enum(TaskType), default=TaskType.normal)

    user: Mapped["User"] = relationship(back_populates="tasks")