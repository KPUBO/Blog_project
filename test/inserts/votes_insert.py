from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.m2m_models.vote import user_post_votes, VoteStatuses


async def query_execution(session: AsyncSession, user_id: int, post_id: int, vote: VoteStatuses):
    query = insert(user_post_votes).values(
        user_id=user_id,
        post_id=post_id,
        vote_type=vote
    )
    await session.execute(query)


user_post_votes_connection = [
    {
        'user_id': 1,
        'post_id': 1,
        'vote': VoteStatuses.like
    },
    {
        'user_id': 2,
        'post_id': 2,
        'vote': VoteStatuses.dislike
    },
    {
        'user_id': 3,
        'post_id': 3,
        'vote': VoteStatuses.like
    },
    {
        'user_id': 4,
        'post_id': 4,
        'vote': VoteStatuses.dislike
    },
    {
        'user_id': 5,
        'post_id': 5,
        'vote': VoteStatuses.like
    },
    {
        'user_id': 5,
        'post_id': 1,
        'vote': VoteStatuses.dislike
    }

]


async def user_post_votes_insert(session: AsyncSession):
    for conn in user_post_votes_connection:
        await query_execution(session,
                              conn['user_id'],
                              conn['post_id'],
                              conn['vote'])
    await session.flush()
