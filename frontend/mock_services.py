from typing import List

import typing

from backend.services.admin import AdminService
from backend.services.poll import PollService, Answer, Poll, PollStats, PollEntity, AnswerStats
from backend.services.user import UserService


class MockAdminService(AdminService):
    def __init__(self):
        self._admins = []
    def authorize(self, password: str, user: str) -> bool:
        print(f"authorizing {user} with password {password}")
        if password == "abracadabra":
            if not user in self._admins:
                self._admins.append(user)
            return True
        return False

    def check_admin(self, user: str) -> bool:
        print(f"checking admin {user}")
        return user in self._admins

class MockPollService(PollService):
    def get_all_polls(self) -> List[PollEntity]:
        return [PollEntity(str(i), p) for i, p in enumerate(self.polls)]

    def __init__(self):
        self.polls = []
        self.stats = {}
    def get_stats(self, poll_id: str) -> typing.Optional[PollStats]:
        return self.stats.get(poll_id)

    def create_poll(self, poll: Poll) -> str:
        print("created new poll: " + str(poll))
        self.polls.append(poll)
        return str(len(self.polls)-1)

    def get_poll(self, poll_id: str) -> typing.Optional[Poll]:
        print("getting poll: " + str(poll_id))
        return self.polls[int(poll_id)]


    def record_answer(self, poll_id: str, question_id: int, answer: Answer) -> None:
        print("recording answer " + answer + " for question " + str(question_id) + " in poll " + poll_id)
        poll = self.get_poll(poll_id)
        if not poll_id in self.stats:
            self.stats[poll_id] = PollStats([(question, AnswerStats(0, 0, 0)) for question in poll.questions])
        if answer == Answer.YES:
            self.stats[poll_id].question_stats[question_id][1].yes += 1
        elif answer == Answer.NO:
            self.stats[poll_id].question_stats[question_id][1].no += 1
        elif answer == Answer.IDK:
            self.stats[poll_id].question_stats[question_id][1].idk += 1
        print(self.stats[poll_id])
        return

class MockUserService(UserService):
    def __init__(self):
        self.users = []
    def get_all_users(self) -> List[str]:
        return self.users

    def add_user(self, user: str):
        if user not in self.users: self.users.append(user)
        print("added user %s" % user)