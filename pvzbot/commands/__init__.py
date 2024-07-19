__all__ = [
    "router",
]
from aiogram import Router

from .admin_commands import router as admin_router
from .common_commands import router as common_router
from .father_commands import router as father_router


router = Router()

# including routers
router.include_router(admin_router)
router.include_router(father_router)
# It goes last as it is common
router.include_router(common_router)
