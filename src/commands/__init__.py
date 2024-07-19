__all__ = [
    "router",
]
from admin_commands import router as admin_router
from aiogram import Router
from common_commands import router as common_router


router = Router()

# including routers
router.include_router(admin_router)

# It goes last as it is common
router.include_router(common_router)
