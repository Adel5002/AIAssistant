from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None)
    interval_seconds: int = Field(default=3600, ge=60) # Минимум 1 минута

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: int
    last_reminded_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)