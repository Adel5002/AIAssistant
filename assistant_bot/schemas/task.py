from enum import Enum
from typing import Self
from pydantic import BaseModel, Field, ConfigDict, model_validator
from datetime import datetime

class TaskType(str, Enum):
    normal = "normal"
    interval = "interval"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = Field(None)
    interval_seconds: int = Field(default=3600, ge=60)
    type: TaskType = Field(default=TaskType.normal)
    is_active: bool = Field(default=True)

    date: datetime | None = Field(None)

    @model_validator(mode="after")
    def check_date_based_on_type(self) -> Self:
        if self.type == TaskType.interval and self.date is None:
            raise ValueError("Для интервальной задачи поле 'date' обязательно!")
        return self

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    user_id: int
    last_reminded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)