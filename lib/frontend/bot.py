
from aiogram import Bot, Dispatcher

from lib.backend.services.services import Services
from lib.frontend.middlewares.admin_middleware import AdminCheckMiddleware
from lib.frontend.routes.poll_answering_route import poll_answering_route, poll_invite_sender_factory
from lib.frontend.routes.poll_creation_route import poll_creation_route
from lib.frontend.routes.poll_sending_route import poll_sending_route
from lib.frontend.routes.poll_stats_route import poll_stats_route
from lib.frontend.routes.start_route import start_route


class BotFrontend:
    def __init__(self, token: str, services: Services):
        self._bot = Bot(token=token)
        self._services = services

    def start(self):
        disp = Dispatcher()
        auth_mw = AdminCheckMiddleware(self._services.admin)
        disp.include_router(start_route(self._services))
        disp.include_router(poll_creation_route(self._services, auth_mw))
        poll_invite_sender = poll_invite_sender_factory(self._bot)
        disp.include_router(poll_sending_route(self._services, poll_invite_sender, auth_mw))
        disp.include_router(poll_answering_route(self._services))
        disp.include_router(poll_stats_route(self._services, auth_mw))
        disp.run_polling(self._bot)


