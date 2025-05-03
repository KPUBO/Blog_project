from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


async def test_get_reactions_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/reactions?limit=5&offset=0",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200
    assert len(reactions) == 5


async def test_get_reactions_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/reactions?limit=5&offset=0")

    assert response.status_code == 401


async def test_get_reaction_by_id_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/reactions/1",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200
    assert reactions['id'] == 1

async def test_get_reaction_by_id_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.get(
        "api/reactions/1")

    assert response.status_code == 401

async def test_get_reaction_by_id_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.get(
        "api/reactions/10",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404

async def test_add_new_reaction_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/reactions",
        json={
            'name': 'New_test_reaction'
        },
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200
    assert reactions['id'] == 6
    assert reactions['name'] == 'New_test_reaction'

async def test_add_new_reaction_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/reactions",
        json={
            'name': 'New_test_reaction'
        })

    assert response.status_code == 401

async def test_add_new_reaction_409(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/reactions",
        json={
            'name': 'Test_Reaction_1'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 409

async def test_update_reaction_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.put(
        "api/reactions/1",
        json={
            'name': 'New_test_reaction'
        },
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200
    assert reactions['id'] == 1
    assert reactions['name'] == 'New_test_reaction'

async def test_update_reaction_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.put(
        "api/reactions/1",
        json={
            'name': 'New_test_reaction'
        })

    assert response.status_code == 401

async def test_update_reaction_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.put(
        "api/reactions/10",
        json={
            'name': 'New_test_reaction'
        },
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404

async def test_delete_reaction_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "api/reactions/1",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200
    assert reactions['id'] == 1

async def test_delete_reaction_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "api/reactions/1")

    assert response.status_code == 401

async def test_delete_reaction_404(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "api/reactions/10",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 404


async def test_leave_reaction_to_comment_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "/api/reactions/leave_reaction/2/1",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200


async def test_leave_reaction_to_comment_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.post(
        "api/reactions/leave_reaction/1/1")

    assert response.status_code == 401


async def test_leave_reaction_to_comment_404_no_comment(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.post(
        "api/reactions/leave_reaction/100",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404



async def test_delete_reaction_to_comment_200(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/reactions/delete_reaction/1",
        headers={'Authorization': f'Bearer {token}'})

    reactions = response.json()

    assert response.status_code == 200


async def test_delete_reaction_to_comment_401(async_client: AsyncClient, async_db: AsyncSession) -> None:
    response = await async_client.delete(
        "/api/reactions/delete_reaction/1")

    assert response.status_code == 401


async def test_delete_reaction_to_comment_404_no_comment(async_client: AsyncClient, async_db: AsyncSession, get_user_token) -> None:
    token = await get_user_token('admin')
    response = await async_client.delete(
        "/api/reactions/delete_reaction/100",
        headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == 404


