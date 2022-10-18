from frontend.bot import BotFrontend, Services
from frontend.mock_services import MockPollService, MockUserService, MockAdminService


async def initialize_bot(token: str) -> BotFrontend:
    services = Services(admin=MockAdminService(), poll=MockPollService(), user=MockUserService())
    bot = BotFrontend(token, services)
    return bot
