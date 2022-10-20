import abc
import dataclasses
import typing
from enum import Enum
from typing import List


class Answer(Enum):
    YES = 1
    NO = 2
    IDK = 3


@dataclasses.dataclass
class Question:
    text: str

@dataclasses.dataclass
class AnswerStats:
    yes: int
    no: int
    idk: int

@dataclasses.dataclass
class PollStats:
    question_stats: List[typing.Tuple[Question, AnswerStats]]

@dataclasses.dataclass
class Poll:
    questions: List[Question]

@dataclasses.dataclass
class PollEntity:
    id: str
    poll: Poll


class PollService(abc.ABC):
    @abc.abstractmethod
    def create_poll(self, poll: Poll) -> str:
        """Creates a Poll with the given properties. Returns the id of the created poll"""
        pass

    @abc.abstractmethod
    def get_poll(self, poll_id: str) -> PollEntity:
        """Returns the poll with the given id"""
        pass

    @abc.abstractmethod
    def record_answer(self, poll_id: str, question_id: str, answer: Answer) -> None:
        """Records the answer to the poll question with the given id"""
        pass

    @abc.abstractmethod
    def get_stats(self, poll_id: str) -> PollStats:
        """Returns the response stats for the poll with the given id"""
        pass

