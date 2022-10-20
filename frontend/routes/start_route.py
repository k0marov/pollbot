from aiogram import types, Router
from aiogram import filters
from backend.services.services import Services

def start_route(services: Services) -> Router:
    router = Router()

    @router.message(filters.Command("start"))
    async def _start(message: types.Message):
        services.user.add_user(str(message.chat.id))
        await message.answer("Ваш id был зарегистрирован в базе данных.")

    @router.message(filters.Command("admin_login"))
    async def _admin_login(message: types.Message):
        password = message.text.removeprefix("/admin_login").strip()
        success = services.admin.authorize(password, str(message.chat.id))
        if success:
            await message.answer("Вы успешно зарегистрировались в качестве админа.")
        else:
            await message.answer("Ошибка - неверный пароль")

    return router



