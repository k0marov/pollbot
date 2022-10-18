import abc


class AdminService(abc.ABC):
    @abc.abstractmethod
    def authorize(self, password: str, user: str) -> bool:
        """
        If the provided password is valid, adds the user to the admins list and returns True.
        Otherwise, returns False.
        """
        pass
    @abc.abstractmethod
    def check_admin(self, user: str) -> bool:
        """Returns True if the specified user is in the admins list, otherwise False"""
        pass

