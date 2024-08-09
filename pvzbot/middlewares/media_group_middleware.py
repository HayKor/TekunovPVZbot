import asyncio
from typing import Any, Awaitable, Callable, Dict, List, Union

from aiogram import BaseMiddleware
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message, TelegramObject


class GetMediaGroupMiddleware(BaseMiddleware):
    album_data: dict[str, List[Message]] = {}

    def __init__(self, latency: int | float = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not event.media_group_id:
            return await handler(event, data)
        flag = get_flag(data, "get_media_group")
        if not flag:
            return await handler(event, data)

        if self.album_data.get(event.media_group_id):
            self.album_data[event.media_group_id].append(event)
        else:
            self.album_data[event.media_group_id] = [event]
            await asyncio.sleep(self.latency)
            data["is_last"] = True
            data["album"] = self.album_data[event.media_group_id]

        try:
            await handler(event, data)
        finally:
            if event.media_group_id and data.get("is_last"):
                del self.album_data[event.media_group_id]
