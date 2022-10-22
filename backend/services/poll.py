import abc
import dataclasses
import typing
from enum import Enum
from typing import List


@dataclasses.dataclass
class Question:
    text: str

@dataclasses.dataclass
class Poll:
    title: str
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
    def get_poll(self, poll_id: str) -> typing.Optional[Poll]:
        """Returns the poll with the given id"""
        pass

    @abc.abstractmethod
    def get_all_polls(self) -> List[PollEntity]:
        pass

