import asyncio
import os
from celery import Celery
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.repositories.posts_repository import PostRepository
from core.config import settings
from core.models import Post
from core.schemas.post import PostCreate
from core.models import db_helper

REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)

redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

DB_URL = os.getenv('APP_CONFIG__DB__URL', 'postgresql+asyncpg://postgres:postgres@localhost:5432/blog_pp')
celery_app = Celery(
    "tasks",
    broker=redis_url,
    backend=redis_url,
)

celery_app.conf.update(
    result_backend='redis://localhost:6379/0',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    SQLALCHEMY_DATABASE_URL=settings.db.url,
)


async def _insert(post):
    async for session in db_helper.session_getter():
        repo = PostRepository(session)
        await repo.scheduling_post_publishing(post)


@celery_app.task
def create_post_task(post: dict):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        task = loop.create_task(_insert(post))
        result = loop.run_until_complete(task)

    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        loop.close()


    return result


