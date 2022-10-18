import abc
import dataclasses
from enum import Enum
from typing import List


class Answer(Enum):
    YES = 1
    NO = 2
    IDK = 3

@dataclasses.dataclass
class Poll:
    questions: List[str]

class PollService(abc.ABC):
    @abc.abstractmethod
    def create_poll(self, poll: Poll) -> str:
        pass
    @abc.abstractmethod
    def get_poll(self, poll_id: str) -> Poll:
        pass
    @abc.abstractmethod
    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        pass

    # TODO
    # @abc.abstractmethod
    # def get_answers(self, poll_id: str) -> :
    #     pass



