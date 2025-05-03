from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_tags_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "api/tags?limit=5&offset=0",
        headers={'Authorization': f'Bearer {token}'})

    tags = response.json()

    assert response.status_code == 200
    assert len(tags) == 5


async def test_get_tags_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/tags?limit=5&offset=0")

    assert response.status_code == 401


async def test_get_tag_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "api/tags/1",
        headers={'Authorization': f'Bearer {token}'})

    tag = response.json()

    assert response.status_code == 200
    assert tag['id'] == 1


async def test_get_tag_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/tags/1")

    assert response.status_code == 401


async def test_get_tag_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/tags/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_get_tag_by_post_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/tags/1/tags",
        headers={'Authorization': f'Bearer {token}'})

    tags = response.json()

    assert response.status_code == 200
    assert len(tags) == 2


async def test_get_tag_by_post_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/tags/1/tags")

    assert response.status_code == 401


async def test_get_tag_by_post_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/tags/10/tags",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_add_tag_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/tags",
        json={
            'name': 'New_test_tag'
        },
        headers={'Authorization': f'Bearer {token}'})

    tag = response.json()

    assert response.status_code == 200
    assert tag['id'] == 6

async def test_add_tag_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "/api/tags",
        json={
            'name': 'New_test_tag'
        })

    assert response.status_code == 401


async def test_add_tag_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/tags",
        json={
            'name': 'Test_Tag_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_update_tag_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/tags/1",
        json={
            'name': 'New_test_tag_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    tag = response.json()

    assert response.status_code == 200
    assert tag['id'] == 1
    assert tag['name'] == 'New_test_tag_1'


async def test_update_tag_401(async_client: AsyncClient, async_db: AsyncSession) -> None:

    response = await async_client.put(
        "/api/tags/1",
        json={
            'name': 'New_test_tag_1'
        })

    assert response.status_code == 401


async def test_update_tag_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/tags/10",
        json={
            'name': 'New_test_tag_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_delete_tag_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/tags/1",
        headers={'Authorization': f'Bearer {token}'})

    tag = response.json()

    assert response.status_code == 200
    assert tag['id'] == 1
    assert tag['name'] == 'Test_Tag_1'

async def test_delete_tag_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/tags/1")

    assert response.status_code == 401


async def test_delete_tag_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/tags/10",
        headers={'Authorization': f'Bearer {token}'})

    tag = response.json()

    assert response.status_code == 404

