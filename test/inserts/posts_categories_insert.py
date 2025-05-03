from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post
from core.models.posts_models.post import Statuses
from core.models import post_category
from core.models import Category


query = text("""
    INSERT INTO posts_categories (post_id, category_id) 
    VALUES (:post_id, :category_id)
""")


post_category_connection = [
    {
        'post_id': 1,
        'category_id': 1
    },
    {
        'post_id': 1,
        'category_id': 5
    },
    {
        'post_id': 2,
        'category_id': 2
    },
    {
        'post_id': 3,
        'category_id': 3
    },
    {
        'post_id': 4,
        'category_id': 4
    },
    {
        'post_id': 5,
        'category_id': 5
    },

]


async def posts_categories_insert(session: AsyncSession):
    for conn in post_category_connection:
        await session.execute(query, conn)
