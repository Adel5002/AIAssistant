from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.models.user import User
from core.database.models.task import Task
from schemas.user import UserCreate, UserRead
from schemas.task import TaskCreate, TaskRead

class StorageService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_user(self, user_data: UserCreate) -> User:
        query = select(User).where(User.id == user_data.id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            user = User(**user_data.model_dump())
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
        return UserRead.model_validate(user)

    async def create_task(self, user_id: int, task_data: TaskCreate) -> TaskRead:
        new_task = Task(
            user_id=user_id,
            **task_data.model_dump()
        )
        self.session.add(new_task)
        await self.session.commit()
        await self.session.refresh(new_task)
        
        return TaskRead.model_validate(new_task)

    async def get_user_tasks(self, user_id: int, only_active: bool = True) -> list[TaskRead]:
        query = select(Task).where(Task.user_id == user_id)
        if only_active:
            query = query.where(Task.is_active)
        
        result = await self.session.execute(query)
        tasks = result.scalars().all()
        return [TaskRead.model_validate(t) for t in tasks]

    async def get_task(self, task_id: int) -> TaskRead | None:
        query = select(Task).where(Task.id == task_id)
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()
        return TaskRead.model_validate(task) if task else None    

    async def deactivate_task(self, task_id: int, user_id: int):
        query = (
            update(Task)
            .where(Task.id == task_id, Task.user_id == user_id)
            .values(is_active=False)
        )
        await self.session.execute(query)
        await self.session.commit()