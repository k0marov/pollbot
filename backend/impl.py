from interface import *


class Service(PollService):
    def __init__(self):
        pass

    def add_user(self, user: str) -> bool:
        pass

    def assign_admin(self):
        pass

    def respond(self, question_id: str, answer: str, from_user: str) -> bool:
        pass

    def get_all_users(self) -> List[str]:
        pass