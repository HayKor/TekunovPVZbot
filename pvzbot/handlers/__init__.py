from aiogram import Router

from .poll_handler import router as poll_handler_router


router = Router(name=__name__)

router.include_router(poll_handler_router)
