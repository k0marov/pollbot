from backend.services.services import Services
from frontend.bot import BotFrontend
from frontend.mock_services import MockPollService, MockUserService, MockAdminService
from frontend.subhandlers.start_subhandler import StartSubhandler


async def initialize_bot(token: str) -> BotFrontend:
    services = Services(admin=MockAdminService(), poll=MockPollService(), user=MockUserService())
    start_route = StartSubhandler(services)
    bot = BotFrontend(token, start_route)
    return bot
