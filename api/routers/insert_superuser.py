import asyncio

import fastapi_users
from fastapi import APIRouter, HTTPException

from actions.create_supersuer import create_superuser

router = APIRouter(
    prefix="/insert_superuser",
    tags=["insert_superuser"],
)

@router.post("/insert_superuser")
async def insert_superuser():
    try:
        superuser = await create_superuser()
        return superuser
    except fastapi_users.exceptions.UserAlreadyExists:
        raise HTTPException(status_code=409, detail="Superuser already exists")

