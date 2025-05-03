from fastapi import APIRouter, Depends

from api.dependencies.deps_utils.utils import get_current_user
from api.routers.categories_router import router as categories_router
from api.routers.posts_router import router as posts_router
from api.routers.reactions_router import router as reactions_router
from api.routers.tags_router import router as tags_router
from api.routers.comments_router import router as comments_router
from api.routers.users_router import router as users_router



router = APIRouter(
    dependencies=[Depends(get_current_user)],
)

router.include_router(categories_router)
router.include_router(posts_router)
router.include_router(reactions_router)
router.include_router(tags_router)
router.include_router(comments_router)
router.include_router(users_router)