from sqlalchemy.ext.asyncio import AsyncSession

from test.inserts.admin_insert import insert_admin_db
from test.inserts.categories_insert import categories_insert
from test.inserts.comments_insert import comments_insert
from test.inserts.posts_categories_insert import posts_categories_insert
from test.inserts.posts_insert import posts_insert
from test.inserts.posts_tags_insert import posts_tags_insert
from test.inserts.reaction_to_comment_insert import reaction_to_comment_insert
from test.inserts.reactions_inserts import reactions_insert
from test.inserts.tags_inserts import tags_insert
from test.inserts.users_inserts import users_insert
from test.inserts.votes_insert import user_post_votes_insert


async def all_models_insert(session: AsyncSession) -> None:
    await insert_admin_db(session)
    await users_insert(session)

    await categories_insert(session)
    await tags_insert(session)

    await posts_insert(session)

    await posts_categories_insert(session)
    await posts_tags_insert(session)

    await reactions_insert(session)
    await comments_insert(session)
    await reaction_to_comment_insert(session)
    await user_post_votes_insert(session)
    
    
