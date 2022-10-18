from aiogram import types

from backend.services.services import Services


class StartSubhandler:
    def __init__(self, services: Services):
        self._services = services

    async def start(self, event: types.Message):
        self._services.user.add_user(event.from_user.id)
        await event.answer("Ваш id был зарегистрирован в базе данных.")

    async def admin_login(self, event: types.Message):
        password = event.text.removeprefix("/admin_login").strip()
        success = self._services.admin.authorize(password, event.from_user.id)
        if success:
            await event.answer("Вы успешно зарегистрировались в качестве админа.")
        else:
            await event.answer("Ошибка - неверный пароль")

