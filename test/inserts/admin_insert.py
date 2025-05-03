from passlib.context import CryptContext
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("admin")

insert_admin = {
    "email": "admin@admin.com",
    "hashed_password": hashed_password,
    "is_active": True,
    "is_superuser": True,
    "is_verified": True
}


async def insert_admin_db(session: AsyncSession):
    user = User(**insert_admin)
    session.add(user)

