
from aiogram import Bot, Dispatcher

from frontend.subhandlers.start_subhandler import StartSubhandler


class BotFrontend:
    def __init__(self, token: str, start_route: StartSubhandler):
        self._bot = Bot(token=token)
        self._start_route = start_route

    async def start(self):
        try:
            disp = Dispatcher(bot=self._bot)
            disp.register_message_handler(self._start_route.start, commands={"start", "restart"})
            disp.register_message_handler(self._start_route.admin_login, commands={"admin_login"})
            await disp.start_polling()
        finally:
            await self._bot.close()


