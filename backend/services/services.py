import dataclasses

from backend.services.admin import AdminService
from backend.services.poll import PollService
from backend.services.user import UserService


@dataclasses.dataclass
class Services:
    poll: PollService
    admin: AdminService
    user: UserService

