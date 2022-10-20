from backend.services.services import Services
from frontend.bot import BotFrontend
from frontend.mock_services import MockPollService, MockUserService, MockAdminService


def initialize_bot(token: str) -> BotFrontend:
    services = Services(admin=MockAdminService(), poll=MockPollService(), user=MockUserService())
    bot = BotFrontend(token, services)
    return bot
