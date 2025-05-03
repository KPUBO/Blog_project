from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Comment


comments = [
    {'user_id': 1,
     'post_id': 1,
     'content': 'Test_content_for_test_post_1'},
    {'user_id': 2,
     'post_id': 2,
     'content': 'Test_content_for_test_post_2'},
    {'user_id': 3,
     'post_id': 3,
     'content': 'Test_content_for_test_post_3'},
    {'user_id': 4,
     'post_id': 4,
     'content': 'Test_content_for_test_post_4'},
    {'user_id': 5,
     'post_id': 5,
     'content': 'Test_content_for_test_post_5'},
    {'user_id': 1,
     'post_id': 1,
     'content': 'Reply_comment',
     'reply_to': 1},
    {'user_id': 2,
     'post_id': 6,
     'content': 'Test_comment_for_author_of_post_deletion'},
]


async def comments_insert(session: AsyncSession):
    comment_models = [Comment(**comment) for comment in comments]
    session.add_all(comment_models)
