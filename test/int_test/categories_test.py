import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

pytestmark = pytest.mark.asyncio


async def test_get_categories_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "api/categories?limit=5&offset=0",
        headers={'Authorization': f'Bearer {token}'})

    categories = response.json()

    assert response.status_code == 200
    assert len(categories) == 5


async def test_get_categories_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/categories?limit=5&offset=0")

    assert response.status_code == 401


async def test_get_category_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.get(
        "api/categories/1",
        headers={'Authorization': f'Bearer {token}'})
    category = response.json()

    assert response.status_code == 200
    assert category['id'] == 1
    assert category['name'] == "Test_Category_1"


async def test_get_category_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/categories/1")

    assert response.status_code == 401


async def test_get_category_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    login_response = await async_client.post("/api/auth/jwt/login", data={
        "username": "admin@admin.com",
        "password": "admin"
    })
    token = login_response.json()["access_token"]

    response = await async_client.get(
        "api/categories/123",
        headers={'Authorization': f'Bearer {token}'})

    category = response.json()

    assert response.status_code == 404


async def test_add_category_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/categories",
        json={'name': 'Test_Category_6'},
        headers={'Authorization': f'Bearer {token}'})

    category = response.json()

    assert response.status_code == 200
    assert category['id'] == 6
    assert category['name'] == "Test_Category_6"


async def test_add_category_401(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    response = await async_client.post(
        "/api/categories",
        json={'name': 'Test_Category_6'})

    assert response.status_code == 401


async def test_add_category_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.post(
        "/api/categories",
        json={'name': 'Test_Category_5'},
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409


async def test_update_category_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/categories/5",
        json={'name': 'New_Test_Category_5'},
        headers={'Authorization': f'Bearer {token}'})

    category = response.json()

    assert response.status_code == 200
    assert category['id'] == 5
    assert category['name'] == "New_Test_Category_5"


async def test_update_category_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "/api/categories/5",
        json={'name': 'New_Test_Category_5'})

    assert response.status_code == 401


async def test_update_category_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.put(
        "/api/categories/7",
        json={'name': 'New_Test_Category_7'},
        headers={'Authorization': f'Bearer {token}'})

    category = response.json()

    assert response.status_code == 404


async def test_delete_category_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/categories/1",
        headers={'Authorization': f'Bearer {token}'})

    category = response.json()

    assert response.status_code == 200
    assert category['id'] == 1
    assert category['name'] == "Test_Category_1"


async def test_delete_category_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/categories/5")

    assert response.status_code == 401


async def test_delete_category_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')

    response = await async_client.delete(
        "/api/categories/8",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404
