from fastapi import APIRouter

from app.routes.route_tags import RouteTags

from . import film_collections, films

router = APIRouter(prefix="/v1", tags=[RouteTags.V1])
router.include_router(films.router)
router.include_router(film_collections.router)
