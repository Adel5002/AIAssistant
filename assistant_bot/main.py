import asyncio
import logging
import sys

from aiogram import Dispatcher

from bot.bot import bot
from core.database.engine import get_session
from schemas.task import TaskCreate
from schemas.user import UserCreate
from services.storage import StorageService

dp = Dispatcher()

async def main() -> None:
    await dp.start_polling(bot)
    # async with get_session() as session:
    #     storage = StorageService(session)

    #     user_data = UserCreate(id=123456789, username="John Doe")
    #     user = await storage.get_or_create_user(user_data)
    #     print("User:", user)

    #     task_data = TaskCreate(title="Sample Task", description="This is a sample task.", type="interval", date="2024-07-01T12:00:00Z")
    #     task = await storage.create_task(user_id=user.id, task_data=task_data)
    #     print("Created Task:", task)

    #     tasks = await storage.get_user_tasks(user_id=user.id)
    #     print("User Tasks:", tasks)

    #     await storage.deactivate_task(task_id=task.id, user_id=user.id)
    #     print(f"Task {task.id} deactivated.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
