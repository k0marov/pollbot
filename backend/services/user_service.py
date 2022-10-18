import abc
from typing import List


class UserService(abc.ABC):
    @abc.abstractmethod
    def get_all_users(self) -> List[str]:
        """Returns a list of all user ids stored in the database"""
        pass

    @abc.abstractmethod
    def add_user(self, user_id: str) -> None:
        """Adds the user_id to the users list. If it already exists, should do nothing (e.g. there should not be any duplicates)"""
        pass
