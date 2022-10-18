from typing import List

from backend.services.admin_service import AdminService
from backend.services.poll_service import PollService, Answer, Poll
from backend.services.user_service import UserService


class MockAdminService(AdminService):
    def authorize(self, password: str, user: str) -> bool:
        return password == "abracadabra"

    def check_admin(self, user: str) -> bool:
        return False

class MockPollService(PollService):
    def create_poll(self, poll: Poll) -> str:
        raise NotImplementedError()

    def get_poll(self, poll_id: str) -> Poll:
        raise NotImplementedError()

    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        raise NotImplementedError()

class MockUserService(UserService):
    def get_all_users(self) -> List[str]:
        raise NotImplementedError()

    def add_user(self, user: str):
        raise NotImplementedError()