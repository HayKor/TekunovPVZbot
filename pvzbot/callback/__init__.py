from aiogram import Router

from .menu_cb import router as menu_router


router = Router(name=__name__)

router.include_router(menu_router)
