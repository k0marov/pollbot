import dataclasses

from lib.backend.services.admin import AdminService
from lib.backend.services.poll import PollService
from lib.backend.services.stats import StatsService
from lib.backend.services.user import UserService


@dataclasses.dataclass
class Services:
    poll: PollService
    admin: AdminService
    user: UserService
    stats: StatsService

