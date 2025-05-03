from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Tag, Post


async def query_execution(session: AsyncSession, post_id: int, tag_id: int):
    try:
        post = await session.get(Post, post_id)
        tag = await session.get(Tag, tag_id)

        await session.refresh(post, ["tag"])

        post.tag = [tag]

        await session.refresh(post, ["tag"])
    except Exception as e:
        print(e)


post_tag_connection = [
    {
        'post_id': 1,
        'tag_id': 1
    },
    {
        'post_id': 1,
        'tag_id': 5
    },
    {
        'post_id': 2,
        'tag_id': 2
    },
    {
        'post_id': 3,
        'tag_id': 3
    },
    {
        'post_id': 4,
        'tag_id': 4
    },
    {
        'post_id': 5,
        'tag_id': 5
    },

]


async def posts_tags_insert(session: AsyncSession):
    for conn in post_tag_connection:
        await query_execution(session, conn['post_id'], conn['tag_id'])
