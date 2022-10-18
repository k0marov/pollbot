import dataclasses

from backend.services.admin_service import AdminService
from backend.services.poll_service import PollService
from backend.services.user_service import UserService


@dataclasses.dataclass
class Services:
    poll: PollService
    admin: AdminService
    user: UserService

