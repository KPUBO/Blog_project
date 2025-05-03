from sqlalchemy.ext.asyncio import AsyncSession

from core.models import UserCommentReaction

reaction_to_comment = [
    {'user_id': 1,
     'comment_id': 1,
     'reaction_id': 1},
    {'user_id': 2,
     'comment_id': 2,
     'reaction_id': 2},
    {'user_id': 3,
     'comment_id': 3,
     'reaction_id': 1},
    {'user_id': 4,
     'comment_id': 4,
     'reaction_id': 4},
    {'user_id': 5,
     'comment_id': 5,
     'reaction_id': 5},
    {'user_id': 6,
     'comment_id': 6,
     'reaction_id': 2},
    {'user_id': 1,
     'comment_id': 7,
     'reaction_id': 1},
]


async def reaction_to_comment_insert(session: AsyncSession):
    reaction_to_comment_models = [UserCommentReaction(**reaction_to_comment_conn) for reaction_to_comment_conn in
                                  reaction_to_comment]
    session.add_all(reaction_to_comment_models)
