import logging
import os
import platform
import subprocess
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from api import router
from api.auth import router as auth_router
from api.router_imports import router as import_routers
from api.routers.insert_superuser import router as insert_superuser_router
from core.config import settings
from core.models.db_helper import db_helper

REDIS_HOST = os.getenv('APP_CONFIG__REDIS_DB__HOST', 'localhost')
REDIS_PORT = os.getenv('APP_CONFIG__REDIS_DB__PORT', 6379)


def start_workers():
    subprocess.Popen(
        ["celery", "-A", "api.scheduling.celery_worker.celery_app", "worker", "--loglevel=info", "--pool=solo"])
    subprocess.Popen(["celery", "-A", "api.scheduling.celery_worker.celery_app", "flower", "--loglevel=info"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}/0")
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
    logger = logging.getLogger("uvicorn")
    current_os = platform.system()
    if current_os == "Windows":
        logger.info(f"Documentation: http://{settings.run.host}:{settings.run.port}/docs")
    if current_os == "Linux":
        logger.info(f"Documentation: http://{settings.run.host}:8001/docs")

    yield
    subprocess.Popen(["celery", "control", "shutdown"])

    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
    default_response_class=ORJSONResponse,
)

main_app.include_router(router,
                        prefix=settings.api.prefix)
main_app.include_router(auth_router,
                        prefix=settings.api.prefix)
main_app.include_router(import_routers,
                        prefix=settings.api.prefix)
main_app.include_router(insert_superuser_router)
if __name__ == '__main__':
    start_workers()
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
