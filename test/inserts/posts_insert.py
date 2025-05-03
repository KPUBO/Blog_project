from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Post
from core.models.posts_models.post import Statuses


posts = [
    {
        'title': 'Test_Title_1',
        'body': 'Test_Body_1',
        'status': Statuses.draft,
        'author_id': 1
    },
    {
        'title': 'Test_Title_2',
        'body': 'Test_Body_2',
        'status': Statuses.draft,
        'author_id': 2
    },
    {
        'title': 'Test_Title_3',
        'body': 'Test_Body_3',
        'status': Statuses.draft,
        'author_id': 3
    },
    {
        'title': 'Test_Title_4',
        'body': 'Test_Body_4',
        'status': Statuses.draft,
        'author_id': 4
    },
    {
        'title': 'Test_Title_5',
        'body': 'Test_Body_5',
        'status': Statuses.draft,
        'author_id': 5
    },
    {
        'title': 'Test_Title_6',
        'body': 'Test_Body_6',
        'status': Statuses.draft,
        'author_id': 6
    },
]


async def posts_insert(session: AsyncSession):
    post_models = [Post(**post) for post in posts]
    session.add_all(post_models)
    await session.flush()
