import redis

from lib.backend.impl.admin import AdminServiceImpl
from lib.backend.impl.poll import PollServiceImpl
from lib.backend.impl.stats import StatsServiceImpl
from lib.backend.impl.user import UserServiceImpl
from lib.backend.services.services import Services
from lib.backend.store.redis_store import RedisStore
from lib.config import Config
from lib.frontend.bot import BotFrontend


def initialize(config: Config) -> BotFrontend:
    client = redis.Redis(host=config.redis_host, port=config.redis_port)
    store = RedisStore(client)
    services = Services(
        admin=AdminServiceImpl(store, config.admin_pass),
        poll=PollServiceImpl(store),
        user=UserServiceImpl(store),
        stats=StatsServiceImpl(store)
    )
    bot = BotFrontend(config.bot_token, services)
    return bot
