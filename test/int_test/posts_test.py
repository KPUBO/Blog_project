from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_posts_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts?limit=5&offset=0",
        headers={'Authorization': f'Bearer {token}'})

    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == 5


async def test_get_posts_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts?limit=5&offset=0")

    posts = response.json()

    assert response.status_code == 401


async def test_get_post_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    post = response.json()

    assert response.status_code == 200
    assert post['post']['id'] == 1
    assert post['post']['title'] == 'Test_Title_1'


async def test_get_post_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts/1")

    assert response.status_code == 401


async def test_get_posts_by_title_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/find/find_posts_by_title?title=Test",
        headers={'Authorization': f'Bearer {token}'})

    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == 6


async def test_get_posts_by_title_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts/find/find_posts_by_title?title=Test")

    assert response.status_code == 401


async def test_get_posts_by_title_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/find/find_posts_by_title?title=QWERTY",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_posts_by_content_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/find/find_posts_by_content?content=Test",
        headers={'Authorization': f'Bearer {token}'})

    posts = response.json()

    assert response.status_code == 200
    assert len(posts) == 6


async def test_get_post_by_content_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts/find/find_posts_by_content?content=Test")

    assert response.status_code == 401


async def test_get_post_by_content_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/find/find_posts_by_content?content=QWERTY",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_post_by_category_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/categories/1/posts",
        headers={'Authorization': f'Bearer {token}'})

    posts = response.json()

    assert response.status_code == 200
    assert posts[0]['post']['id'] == 1


async def test_get_post_by_category_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts/categories/1/posts")

    assert response.status_code == 401


async def test_get_post_by_category_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/categories/100/posts",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_post_by_tag_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/tags/1/posts",
        headers={'Authorization': f'Bearer {token}'})

    posts = response.json()

    assert response.status_code == 200
    assert posts[0]['post']['id'] == 1


async def test_get_post_by_tag_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/posts/tags/1/posts")

    assert response.status_code == 401


async def test_get_post_by_tag_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/posts/tags/100/posts",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_link_post_and_category_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/category/2/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_link_post_and_category_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/posts/link/category/1/posts/1")

    assert response.status_code == 401


async def test_link_post_and_category_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.post(
        "api/posts/link/category/2/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_link_post_and_category_404_post_not_found(async_client: AsyncClient, async_db: AsyncSession,
                                                         get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.post(
        "api/posts/link/category/2/posts/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_link_post_and_category_404_category_not_found(async_client: AsyncClient, async_db: AsyncSession,
                                                             get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/category/10/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_link_post_and_category_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/category/1/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_link_post_and_tag_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/tag/2/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_link_post_and_tag_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/posts/link/tag/1/posts/1")

    assert response.status_code == 401


async def test_link_post_and_tag_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.post(
        "api/posts/link/tag/2/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_link_post_and_tag_404_post_not_found(async_client: AsyncClient, async_db: AsyncSession,
                                                    get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.post(
        "api/posts/link/tag/2/posts/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_link_post_and_tag_404_tag_not_found(async_client: AsyncClient, async_db: AsyncSession,
                                                   get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/tag/10/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_link_post_and_tag_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts/link/tag/1/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_add_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts",
        json={
            'title': 'Added_test_title_1',
            'body': 'Added_test_body_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_add_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/posts",
        json={
            'title': 'Added_test_title_1',
            'body': 'Added_test_body_1'
        })

    assert response.status_code == 401


async def test_add_post_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/posts",
        json={
            'title': 'Test_Title_1',
            'body': 'Test_Body_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_update_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.put(
        "/api/posts/1",
        json={"title": "string123",
              "body": "string123",
              "status": "draft"},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_update_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "/api/posts/1",
        json={"title": "string123",
              "body": "string123",
              "status": "draft"})

    assert response.status_code == 401


async def test_update_post_403_non_author(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.put(
        "/api/posts/1",
        json={"title": "string123",
              "body": "string123",
              "status": "draft"},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_update_post_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.put(
        "/api/posts/1",
        json={"title": "Test_Title_2",
              "body": "Test_Body_2",
              "status": "draft"},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_update_post_422(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.put(
        "/api/posts/1",
        json={"title": "new_Test_Title_2",
              "body": "new_Test_Body_2"},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422


async def test_delete_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    post_to_delete = response.json()

    assert response.status_code == 200
    assert post_to_delete['id'] == 1


async def test_delete_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/posts/1")
    assert response.status_code == 401


async def test_delete_post_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.delete(
        "/api/posts/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delete_post_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/100",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delink_post_and_category_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/1/category/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_delink_post_and_category_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/posts/1/category/1/delete_link")

    assert response.status_code == 401


async def test_delink_post_and_category_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.delete(
        "/api/posts/1/category/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delink_post_and_category_404_no_post(async_client: AsyncClient, async_db: AsyncSession,
                                                    get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/10/category/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delink_post_and_category_404_no_category(async_client: AsyncClient, async_db: AsyncSession,
                                                        get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/1/category/10/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delink_post_and_tag_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/1/tag/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_delink_post_and_tag_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/posts/1/tag/1/delete_link")

    assert response.status_code == 401


async def test_delink_post_and_tag_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')
    response = await async_client.delete(
        "/api/posts/1/tag/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_delink_post_and_tag_404_no_post(async_client: AsyncClient, async_db: AsyncSession,
                                               get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/10/tag/1/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delink_post_and_tag_404_no_category(async_client: AsyncClient, async_db: AsyncSession,
                                                   get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/1/tag/10/delete_link",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_vote_for_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "/api/posts/vote-for-post/2?vote=1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_vote_for_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/posts/vote-for-post/2?vote=1")

    assert response.status_code == 401


async def test_vote_for_post_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "/api/posts/vote-for-post/10?vote=1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_vote_for_post_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "/api/posts/vote-for-post/1?vote=1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_delete_vote_for_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/posts/delete-vote-for-post/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_delete_vote_for_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/posts/delete-vote-for-post/1")

    assert response.status_code == 401


async def test_delete_vote_for_post_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser5')
    response = await async_client.delete(
        "/api/posts/delete-vote-for-post/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_publish_post_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.patch(
        "/api/posts/publish_post/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 200


async def test_publish_post_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.patch(
        "/api/posts/publish_post/1")

    assert response.status_code == 401


async def test_publish_post_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser5')
    response = await async_client.patch(
        "/api/posts/publish_post/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_publish_post_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.patch(
        "/api/posts/publish_post/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_publish_post_400(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    await async_client.patch(
        "/api/posts/publish_post/1",
        headers={'Authorization': f'Bearer {token}'})

    response = await async_client.patch(
        "/api/posts/publish_post/1",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400
