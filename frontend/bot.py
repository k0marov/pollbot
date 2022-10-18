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
        await event.answer(
            f"Hello, {event.from_user.get_mention(as_html=True)} 👋!",
            parse_mode=types.ParseMode.HTML,
        )
    async def _admin_login(self, event: types.Message):
        password = event.text.removeprefix("/admin_login").strip()
        if self._services.admin.check_admin_pass(password):
            self._services.assign_admin(event.from_user.id)

    async def start(self):
        try:
            disp = Dispatcher(bot=self._bot)
            disp.register_message_handler(self._start_handler, commands={"start", "restart"})
            disp.register_message_handler(self._admin_login, commands={"admin_login"})
            await disp.start_polling()
        finally:
            await self._bot.close()


