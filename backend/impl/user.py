import json
from typing import List

from backend.services import user
from backend.store import store


class UserServiceImpl(user.UserService):
    _USERS_KEY = 'users'

    def __init__(self, s: store.Store):
        self._store = s

    def get_all_users(self) -> List[str]:
        result = self._store.get(UserServiceImpl._USERS_KEY)
        return result if result else []

    def add_user(self, user_id: str) -> None:
        users = self.get_all_users()
        if user_id in users: return
        users.append(user_id)
        self._store.set(UserServiceImpl._USERS_KEY, users)

