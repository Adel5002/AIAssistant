import asyncio
import os

from datetime import datetime, timezone

from taskiq_redis import RedisAsyncResultBackend
from taskiq.schedule_sources import LabelScheduleSource
from taskiq import TaskiqScheduler
from taskiq_aio_pika import AioPikaBroker, Queue, QueueType

from core.database.engine import get_session
from schemas.task import TaskCreate
from schemas.user import UserCreate
from services.storage import StorageService

from bot.bot import bot

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

broker = AioPikaBroker(
    "amqp://guest:guest@rabbitmq:5672",
    delay_queue=Queue(
        name="taskiq_delay",
        declare=True,
        type=QueueType.CLASSIC
    ),
).with_result_backend(RedisAsyncResultBackend(redis_url))

scheduler = TaskiqScheduler(broker, sources=[LabelScheduleSource(broker)])


@broker.task(task_name="start_task_traking")
async def start_task_traking(task_id: int):
    async with get_session() as session:
        storage = StorageService(session)
        task = await storage.get_task(task_id)
        if not task:
            print(f"--- Task with ID {task_id} not found. Skipping scheduling. ---")
            return
        elif not task.is_active:
            print(f"--- Task with ID {task_id} is inactive. Skipping scheduling. ---")
            return
        
        if task.type == "normal":
            await normal_task_reminder.kicker().with_labels(delay=task.interval_seconds).kiq(task_id=task_id)
        elif task.type == "interval":
            now = datetime.now(timezone.utc)
            seconds = (task.date - now).total_seconds()
            await interval_task_reminder.kicker().with_labels(delay=seconds).kiq(task_id=task_id)


@broker.task(task_name="normal_task_reminder")
async def normal_task_reminder(task_id: int):
    print(f"--- Normal Task Reminder triggered for task ID: {task_id} ---")
    async with get_session() as session:
        storage = StorageService(session)
        task = await storage.get_task(task_id)
        
        message = f"Напоминание о задаче: {task.title}\nОписание: {task.description}"
        await bot.send_message(task.user_id, message)

    await normal_task_reminder.kicker().with_labels(delay=task.interval_seconds).kiq(task_id=task_id)


@broker.task(task_name="interval_task_reminder")
async def interval_task_reminder(task_id: int):
    async with get_session() as session:
        storage = StorageService(session)
        task = await storage.get_task(task_id)

        message = f"Напоминание о интервальной задаче: {task.title}\nОписание: {task.description}"
        await bot.send_message(task.user_id, message)
    
    now = datetime.now(timezone.utc)
    seconds = (task.date - now).total_seconds()
    await interval_task_reminder.kicker().with_labels(delay=seconds).kiq(task_id=task_id)
    

async def create_test_user_with_minute_task():
    await broker.startup()
    async with get_session() as session:
        storage = StorageService(session)

        user_data = UserCreate(
            id=5645916737, 
            username="Adel_Dev" 
        )
        user = await storage.get_or_create_user(user_data)
        print(f"--- User processed: {user.username} (ID: {user.id}) ---")

        task_data = TaskCreate(
            title="Ежеминутный пуш",
            description="Тестовая задача, которая пинается раз в минуту",
            type="normal",
            interval_seconds=60,
        )

        task = await storage.create_task(user_id=user.id, task_data=task_data)
        print(f"--- Task created: {task.title} (ID: {task.id}) ---")

        await start_task_traking.kicker().kiq(task_id=task.id)
        
        print(f"--- Taskiq: Диспетчер запущен для таски {task.id} ---")


if __name__ == "__main__":
    asyncio.run(create_test_user_with_minute_task())
