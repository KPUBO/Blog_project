from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_comments_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("admin")

    response = await async_client.get(
        "api/comments?limit=5&offset=0",
        headers={'Authorization': f'Bearer {token}'})

    comments = response.json()

    assert response.status_code == 200
    assert len(comments) == 5


async def test_get_comments_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "api/comments?limit=5&offset=0")

    assert response.status_code == 401


async def test_get_comment_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("admin")

    response = await async_client.get(
        "api/comments/1",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 1
    assert comment['post_id'] == 1
    assert comment["content"] == "Test_content_for_test_post_1"


async def test_get_comment_by_id_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.get(
        "api/comments/1")

    assert response.status_code == 401


async def test_post_comment_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("admin")

    response = await async_client.post(
        "api/comments",
        json={
            'post_id': 1,
            'content': 'Additional_test_content_for_test_post_1',
            'reply_to': None
        },
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 8
    assert comment['post_id'] == 1
    assert comment['content'] == 'Additional_test_content_for_test_post_1'


async def test_post_comment_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.post(
        "api/comments")

    assert response.status_code == 401


async def test_update_comment_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("admin")

    response = await async_client.put(
        "api/comments/1",
        json={
            'content': 'New_test_content_for_test_post_1',
        },
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 1


async def test_update_comment_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.put(
        "api/comments/1",
    )

    assert response.status_code == 401


async def test_update_comment_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    login_response = await async_client.post("/api/auth/jwt/login", data={
        "username": "testuser1@testuser1.com",
        "password": "testuser1"
    })
    token = login_response.json()["access_token"]

    response = await async_client.put(
        "api/comments/1",
        json={
            'content': 'New_test_content_for_test_post_1_from_user_1',
        },
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 403


async def test_update_comment_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    login_response = await async_client.post("/api/auth/jwt/login", data={
        "username": "testuser1@testuser1.com",
        "password": "testuser1"
    })
    token = login_response.json()["access_token"]

    response = await async_client.put(
        "api/comments/10",
        json={
            'content': 'New_test_content_for_test_post_1_from_user_1',
        },
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 404


async def test_admin_deletion_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("admin")

    response = await async_client.delete(
        "api/comments/5",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 5


async def test_post_author_comment_deletion_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("testuser1")

    response = await async_client.delete(
        "api/comments/2",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 2


async def test_delete_own_comment_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("testuser2")

    response = await async_client.delete(
        "api/comments/3",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 200
    assert comment["id"] == 3


async def test_delete_comment_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.delete(
        "api/comments/1")

    assert response.status_code == 401


async def test_delete_comment_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("testuser5")

    response = await async_client.delete(
        "api/comments/1",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 403


async def test_delete_comment_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token("testuser5")

    response = await async_client.delete(
        "api/comments/100",
        headers={'Authorization': f'Bearer {token}'})

    comment = response.json()

    assert response.status_code == 404
