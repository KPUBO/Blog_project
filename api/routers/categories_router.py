from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from api.dependencies.entity_finder import get_entity_by_id
from api.services.categories_service import CategoryService
from core.schemas.category import CategoryRead, CategoryCreate
from core.models import Category, Post

router = APIRouter(
    prefix='/categories',
    tags=['Categories'],
)


@router.get('',
            response_model=List[CategoryRead],
            summary='Get all categories')
@cache(expire=60)
async def read_categories(
        limit: int = 10,
        offset: int = 0,
        service: CategoryService = Depends()
):
    categories = await service.get_all(offset=offset, limit=limit)
    return categories


@router.get('/{category_id}',
            dependencies=[Depends(get_entity_by_id(Category, 'category_id'))],
            summary='Get category by it\'s id')
async def read_category_by_id(
        category_id: int,
        service: CategoryService = Depends()

):
    category = await service.get_by_id(category_id)
    return category


@router.get('/categories/{post_id}',
            dependencies=[Depends(get_entity_by_id(Post, 'post_id'))],
            response_model=List[CategoryRead],
            summary='Get category by it\'s id'
            )
async def get_categories_by_post_id(
        post_id: int,
        service: CategoryService = Depends()
):
    category = await service.get_categories_by_post_id(post_id)
    return category


@router.post('',
             response_model=CategoryRead,
             summary='Add category to database')
async def add_category(
        category: CategoryCreate,
        service: CategoryService = Depends()
):
    category = service.insert_item(category=category)
    return await category


@router.put('/{category_id}',
            dependencies=[Depends(get_entity_by_id(Category, 'category_id'))],
            response_model=CategoryRead,
            summary='Update category by it\'s id')
async def update_category(
        category_id: int,
        category: CategoryCreate,
        service: CategoryService = Depends()
):
    category = service.update_item(category_id=category_id, category=category)
    return await category


@router.delete('/{category_id}',
               dependencies=[Depends(get_entity_by_id(Category, 'category_id'))],
               response_model=CategoryRead,
               summary='Get category by it\'s id')
async def delete_category(
        category_id: int,
        service: CategoryService = Depends()
):
    category = await service.delete_item(category_id=category_id)
    return category
