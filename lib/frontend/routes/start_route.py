from aiogram import types, Router
from aiogram import filters
from lib.backend.services.services import Services
from lib.frontend.design.texts import Texts


def start_route(services: Services) -> Router:
    router = Router()

    @router.message(filters.Command("start"))
    async def _start(message: types.Message):
        services.user.add_user(str(message.chat.id))
        await message.answer(Texts.GREET)

    @router.message(filters.Command("admin_login"))
    async def _admin_login(message: types.Message):
        password = message.text.removeprefix("/admin_login").strip()
        success = services.admin.authorize(password, str(message.chat.id))
        if success:
            await message.answer(Texts.ADMIN_LOGIN_SUCCESS)
        else:
            await message.answer(Texts.ADMIN_LOGIN_FAIL)

    return router



