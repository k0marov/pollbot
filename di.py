from frontend.bot import BotFrontend
from frontend.mock_services import MockPollService


async def initialize_bot(token: str) -> BotFrontend:
    service = MockPollService()
    bot = BotFrontend(token, service)
    return bot
