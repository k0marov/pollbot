import abc
from typing import List


class UserService(abc.ABC):
    @abc.abstractmethod
    def get_all_users(self) -> List[str]:
        pass
    @abc.abstractmethod
    def add_user(self, user: str):
        pass

