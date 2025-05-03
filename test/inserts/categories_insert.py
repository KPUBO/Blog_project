from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Category

categories = [
    {'name': 'Test_Category_1'},
    {'name': 'Test_Category_2'},
    {'name': 'Test_Category_3'},
    {'name': 'Test_Category_4'},
    {'name': 'Test_Category_5'},
]


async def categories_insert(session: AsyncSession):
    category_models = [Category(**category) for category in categories]
    session.add_all(category_models)
