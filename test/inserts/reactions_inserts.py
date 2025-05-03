from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Reaction


reactions = [
    {'name': 'Test_Reaction_1'},
    {'name': 'Test_Reaction_2'},
    {'name': 'Test_Reaction_3'},
    {'name': 'Test_Reaction_4'},
    {'name': 'Test_Reaction_5'},
]


async def reactions_insert(session: AsyncSession):
    reaction_models = [Reaction(**reaction) for reaction in reactions]
    session.add_all(reaction_models)
    await session.flush()
