import abc


class PollService(abc.ABC):
    @abc.abstractmethod
    def get_all_users(self) -> List[str]:
        pass
    @abc.abstractmethod
    def add_user(self, user: str) -> bool:
        pass
    @abc.abstractmethod
    def assign_admin(self):
        pass
    @abc.abstractmethod
    def respond(self, question_id: str, answer: str, from_user: str) -> bool:
        pass
