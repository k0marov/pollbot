from typing import List

from backend.services.poll_service import PollStats
from services.admin_service import AdminService
from services.user_service import UserService
from services.poll_service import PollService, Poll, AnswerStats, Answer, Question, PollStats
from database import JsonDatabase


class AdminServiceImpl(AdminService):
    def __init__(self, password: str):
        self.password = password
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
    database = JsonDatabase('json_data/polls.json')

    def create_poll(self, poll: Poll) -> str:
        polls = self.database.get().response["Data"]
        if not (poll.title in polls):
            questions = {}
            for i, q in enumerate(poll.questions):
                questions[i]({"text": q.text, "answers": {str(Answer.YES): 0, str(Answer.NO): 0, str(Answer.IDK): 0}})
            polls[poll.title] = {"title": poll.title, "questions": questions}
            self.database.push(polls)
        return poll.title

    def get_poll(self, poll_id: str) -> Poll:
        data = self.database.get().response["Data"][poll_id]
        questions = []
        for k, v in data["questions"].items():
            questions.append(Question(v["text"]))
        return Poll(data["title"], questions)

    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        data = self.database.get().response["Data"]
        data[poll_id]["questions"][question_id]["answers"][str(answer)] += 1
        self.database.push(data)

    def get_stats(self, poll_id: str) -> PollStats:
        data = self.database.get().response["Data"]
        questions = self.get_poll(poll_id).questions
        answers = []
        for i, q in enumerate(questions):
            answer = data[poll_id]["questions"][i]["answers"]
            answers.append((q, AnswerStats(answer[str(Answer.YES)], answer[str(Answer.NO)], answer[str(Answer.IDK)])))
        return PollStats(answers)
