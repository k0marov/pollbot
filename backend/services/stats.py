import abc
import dataclasses
from enum import Enum
from typing import List

import typing

from backend.services.poll import Question


class Answer(str, Enum):
    YES = "YES"
    NO = "NO"
    IDK = "IDK"

@dataclasses.dataclass
class AnswerStats:
    yes: int
    no: int
    idk: int


@dataclasses.dataclass
class PollStats:
    question_stats: typing.List[AnswerStats]


class StatsService(abc.ABC):
    # TODO: stop accepting poll_len here since it is ugly
    @abc.abstractmethod
    def record_answer(self, poll_id: str, question_id: int, answer: Answer, poll_len: int) -> None:
        """Records the answer to the poll question with the given id"""
        pass

    @abc.abstractmethod
    def get_stats(self, poll_id: str) -> typing.Optional[PollStats]:
        """Returns the response stats for the poll with the given id"""
        pass
