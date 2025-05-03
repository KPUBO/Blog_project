from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tag

tags = [
    {'name': 'Test_Tag_1'},
    {'name': 'Test_Tag_2'},
    {'name': 'Test_Tag_3'},
    {'name': 'Test_Tag_4'},
    {'name': 'Test_Tag_5'},
]


async def tags_insert(session: AsyncSession):
    tag_models = [Tag(**tag) for tag in tags]
    session.add_all(tag_models)

    await session.flush()
