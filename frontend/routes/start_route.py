from aiogram import types, Router
from aiogram.filters import Command

from backend.services.services import Services

def start_route(services: Services) -> Router:
    router = Router()

    @router.message(Command("start"))
    async def _start(event: types.Message):
        services.user.add_user(str(event.from_user.id))
        await event.answer("Ваш id был зарегистрирован в базе данных.")

    @router.message(Command("admin_login"))
    async def _admin_login(event: types.Message):
        password = event.text.removeprefix("/admin_login").strip()
        success = services.admin.authorize(password, str(event.from_user.id))
        if success:
            await event.answer("Вы успешно зарегистрировались в качестве админа.")
        else:
            await event.answer("Ошибка - неверный пароль")

    return router



