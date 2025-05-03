from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def testusers_me_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/users/me",
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 1
    assert cur_user['email'] == 'admin@admin.com'

async def testusers_me_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/users/me")

    assert response.status_code == 401

async def test_patch_current_user_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/me",
        json={
            'email': 'newadmin@newadmin.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 1
    assert cur_user['email'] == 'newadmin@newadmin.com'


async def test_patch_current_user_422(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/me",
        json={
            'email': 'new_admin@new_admin.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422


async def test_patch_current_user_400(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/me",
        json={
            'email': 'testuser1@testuser1.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400


async def test_patch_current_user_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.patch(
        "/api/users/me",
        json={
            'email': 'testuser1@testuser1.com',
        })

    assert response.status_code == 401


async def test_get_user_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/users/2",
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 2
    assert cur_user['email'] == 'testuser1@testuser1.com'

async def test_get_user_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "/api/users/2")
    assert response.status_code == 401


async def test_get_user_by_id_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')

    response = await async_client.get(
        "/api/users/2",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_get_user_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "/api/users/20",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_patch_user_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/2",
        json={
            'email': 'newtestuser1@newtestuser1.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    cur_user = response.json()

    assert response.status_code == 200
    assert cur_user['id'] == 2
    assert cur_user['email'] == 'newtestuser1@newtestuser1.com'


async def test_patch_user_by_id_400(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/2",
        json={
            'email': 'testuser2@testuser2.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 400


async def test_patch_user_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:

    response = await async_client.patch(
        "/api/users/2")

    assert response.status_code == 401


async def test_patch_user_by_id_403(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('testuser1')

    response = await async_client.patch(
        "/api/users/2",
        json={
            'email': 'newtestuser1@newtestuser1.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 403


async def test_patch_user_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/20",
        json={
            'email': 'newtestuser1@newtestuser1.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


async def test_patch_user_by_id_422(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.patch(
        "/api/users/2",
        json={
            'email': 'newtestuser1@new_testuser1.com',
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 422


