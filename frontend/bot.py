import dataclasses

from aiogram import Bot, Dispatcher, types

from backend.services.admin_service import AdminService
from backend.services.poll_service import PollService
from backend.services.user_service import UserService


@dataclasses.dataclass
class Services:
    poll: PollService
    admin: AdminService
    user: UserService

class BotFrontend:
    def __init__(self, token: str, services: Services):
        self._bot = Bot(token=token)
        self._services = services

    async def _start_handler(self, event: types.Message):
        self._services.user.add_user(event.from_user.id)
        await event.answer("Ваш id был зарегистрирован в базе данных.")
    async def _admin_login(self, event: types.Message):
        password = event.text.removeprefix("/admin_login").strip()
        success = self._services.admin.authorize(password, event.from_user.id)
        if success:
            await event.answer("Вы успешно зарегистрировались в качестве админа.")
        else:
            await event.answer("Ошибка - неверный пароль")

    async def start(self):
        try:
            disp = Dispatcher(bot=self._bot)
            disp.register_message_handler(self._start_handler, commands={"start", "restart"})
            disp.register_message_handler(self._admin_login, commands={"admin_login"})
            await disp.start_polling()
        finally:
            await self._bot.close()


