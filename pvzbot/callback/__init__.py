from aiogram import Router

from .admin_cb import router as admin_router
from .menu_cb import router as menu_router


router = Router(name=__name__)

router.include_routers(
    menu_router,
    admin_router,
)
