import dataclasses
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware, types

from backend.services.admin import AdminService

# TODO: somehow remove code duplication

class AdminCheckMessageMiddleware(BaseMiddleware):
    def __init__(self, service: AdminService):
        self._service = service
    async def __call__(
        self, handler: Callable[[types.Message, Dict[str, Any]], Awaitable[Any]],
        event: types.Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = str(event.chat.id)
        if self._service.check_admin(user_id):
            return await handler(event, data)
        else:
            await event.answer("Чтобы выполнить это действие, нужно быть админом. Введите /admin_login")
            print("ignoring event because user does not have admin rights")
            return None

class AdminCheckCBMiddleware(BaseMiddleware):
    def __init__(self, service: AdminService):
        self._service = service
    async def __call__(
            self,
            handler: Callable[[types.CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: types.CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = str(event.message.chat.id) # TODO: think about whether this id behavior can lead to exploits
        if self._service.check_admin(user_id):
            return await handler(event, data)
        else:
            await event.answer("Чтобы выполнить это действие, нужно быть админом. Введите /admin_login")
            print("ignoring event because user does not have admin rights")
            return None

class AdminCheckMiddleware:
    def __init__(self, service: AdminService):
        self.msg = AdminCheckMessageMiddleware(service)
        self.cb = AdminCheckCBMiddleware(service)

