from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = [
    {
        "email": "testuser1@testuser1.com",
        "hashed_password": pwd_context.hash("testuser1"),
        "is_active": True,
        "is_superuser": False,
        "is_verified": True
    },
    {
        "email": "testuser2@testuser2.com",
        "hashed_password": pwd_context.hash("testuser2"),
        "is_active": True,
        "is_superuser": False,
        "is_verified": True
    },
    {
        "email": "testuser3@testuser3.com",
        "hashed_password": pwd_context.hash("testuser3"),
        "is_active": True,
        "is_superuser": False,
        "is_verified": True
    },
    {
        "email": "testuser4@testuser4.com",
        "hashed_password": pwd_context.hash("testuser4"),
        "is_active": True,
        "is_superuser": False,
        "is_verified": True
    },
    {
        "email": "testuser5@testuser5.com",
        "hashed_password": pwd_context.hash("testuser5"),
        "is_active": True,
        "is_superuser": False,
        "is_verified": True
    },
]


async def users_insert(session: AsyncSession):
    user_models = [User(**user) for user in users]
    session.add_all(user_models)
    await session.flush()



