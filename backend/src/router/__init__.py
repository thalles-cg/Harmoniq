from fastapi import APIRouter

from .health import router as health_router
from .nota import router as nota_router

router = APIRouter()

router.include_router(health_router)
router.include_router(nota_router)