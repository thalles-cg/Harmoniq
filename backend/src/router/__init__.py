from fastapi import APIRouter

from .health import router as health_router
from .nota import router as nota_router
from .acorde import router as acorde_router
from .musica import router as musica_router
from .usuario import router as usuario_router

router = APIRouter()

router.include_router(health_router)
router.include_router(nota_router)
router.include_router(acorde_router)
router.include_router(musica_router)
router.include_router(usuario_router)