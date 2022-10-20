
from aiogram import Bot, Dispatcher

from backend.services.services import Services
from frontend.routes.poll_creation_route import poll_creation_route
from frontend.routes.poll_sending_route import poll_sending_route
from frontend.routes.start_route import start_route


class BotFrontend:
    def __init__(self, token: str, services: Services):
        self._bot = Bot(token=token)
        self._services = services

    def start(self):
        disp = Dispatcher()
        disp.include_router(start_route(self._services))
        disp.include_router(poll_creation_route(self._services))
        disp.include_router(poll_sending_route(self._services))
        disp.run_polling(self._bot)


