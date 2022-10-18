from backend.services.services import Services
from frontend.bot import BotFrontend
from frontend.mock_services import MockPollService, MockUserService, MockAdminService
from frontend.routes.start_route import StartRoute


async def initialize_bot(token: str) -> BotFrontend:
    services = Services(admin=MockAdminService(), poll=MockPollService(), user=MockUserService())
    start_route = StartRoute(services)
    bot = BotFrontend(token, start_route)
    return bot
