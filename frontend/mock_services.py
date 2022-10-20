from typing import List

from backend.services.admin_service import AdminService
from backend.services.poll_service import PollService, Answer, Poll, PollStats
from backend.services.user_service import UserService


class MockAdminService(AdminService):
    def authorize(self, password: str, user: str) -> bool:
        return password == "abracadabra"

    def check_admin(self, user: str) -> bool:
        return False

class MockPollService(PollService):
    def __init__(self):
        self.polls = []
    def get_stats(self, poll_id: str) -> PollStats:
        pass

    def create_poll(self, poll: Poll) -> str:
        print("created new poll: " + str(poll))
        self.polls.append(poll)
        return str(len(self.polls)-1)

    def get_poll(self, poll_id: str) -> Poll:
        print("getting poll: " + str(poll_id))
        return self.polls[int(poll_id)]


    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        raise NotImplementedError()

class MockUserService(UserService):
    def __init__(self):
        self.users = []
    def get_all_users(self) -> List[str]:
        return self.users

    def add_user(self, user: str):
        self.users.append(user)
        print("added user %s" % user)