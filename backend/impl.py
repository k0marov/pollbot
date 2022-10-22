from typing import List

from backend.services.poll_service import PollStats
from services.admin_service import AdminService
from services.user_service import UserService
from services.poll_service import PollService, Poll, AnswerStats, Answer, Question
import random
import string
from database import JsonDatabase
import dotenv


class AdminServiceImpl(AdminService):
    def __init__(self):
        self.password = dotenv.get_key("env/.env", "PASSWORD")
        self.database = JsonDatabase("json_data/admins.json")

    def authorize(self, password: str, user: str) -> bool:
        if self.password == password:
            data = self.database.get()
            if not (user in data.response["Data"]):
                self.database.push(data.response["Data"] + [user])
            # log here
            return True
        # log here
        return False

    def check_admin(self, user: str) -> bool:
        data = self.database.get()
        if user in data.response["Data"]:
            return True
        return False


class UserServiceImpl(UserService):

    def __init__(self):
        self.database = JsonDatabase("json_data/users.json")
        self.data = []

    def get_all_users(self) -> List[str]:
        return self.database.get().response["Data"]

    def add_user(self, user_id: str) -> None:
        self.data = self.database.get().response["Data"]
        if not (user_id in self.data):
            self.database.push(self.data + [user_id])


class PollServiceImpl(PollService):
    alphabet = string.ascii_letters + string.digits
    size = 20
    database = JsonDatabase('json_data/polls.json')

    def create_poll(self, poll: Poll) -> str:
        identifier = "".join([random.choice(self.alphabet) for _ in range(self.size)])
        polls = self.database.get()
        polls[identifier] = [poll.title, poll.questions]
        return identifier

    def get_poll(self, poll_id: str) -> Poll:
        pass

    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        pass

    def get_stats(self, poll_id: str) -> PollStats:
        pass


service = PollServiceImpl()
print(service.create_poll(Poll("", [])))
