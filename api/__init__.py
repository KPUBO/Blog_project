from fastapi import APIRouter

from api.auth import router as auth_router
from api.dependencies.authentication.fastapi_users import fastapi_users
from core.schemas.user import UserRead, UserUpdate
from api.routers.users_router import router as users_router

router = APIRouter(prefix="/users", tags=["Users"])

router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))

