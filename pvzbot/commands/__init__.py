__all__ = [
    "router",
]
from aiogram import Router

from .admin_commands import router as admin_router
from .common_commands import router as common_router


router = Router()

# including routers
router.include_router(admin_router)

# It goes last as it is common
router.include_router(common_router)
