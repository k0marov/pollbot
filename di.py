import redis

from backend.impl.admin import AdminServiceImpl
from backend.impl.poll import PollServiceImpl
from backend.impl.user import UserServiceImpl
from backend.services.services import Services
from backend.store.redis_store import RedisStore
from frontend.bot import BotFrontend
from frontend.mock_services import MockPollService, MockUserService, MockAdminService


def initialize_bot(token: str) -> BotFrontend:
    client = redis.Redis(host="localhost", port=6379)
    store = RedisStore(client)
    password = "abc"
    services = Services(admin=AdminServiceImpl(store, password), poll=PollServiceImpl(store), user=UserServiceImpl(store), stats=MockPollService())
    bot = BotFrontend(token, services)
    return bot
