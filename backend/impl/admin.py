from typing import List

from backend.services import admin
from backend.store import store


class AdminServiceImpl(admin.AdminService):
    def __init__(self, s: store.Store, password: str):
        self._store = s
        self._password = password

    _ADMINS_KEY = 'admins'

    def authorize(self, password: str, user: str) -> bool:
        if password == self._password:
            self._add_admin(user)
            return True
        return False

    def check_admin(self, user: str) -> bool:
        return user in self._get_all_admins()


    def _get_all_admins(self) -> List[str]:
        result = self._store.get(AdminServiceImpl._ADMINS_KEY)
        return result if result else []

    def _add_admin(self, user_id: str) -> None:
        users = self._get_all_admins()
        if user_id in users: return
        users.append(user_id)
        self._store.set(AdminServiceImpl._ADMINS_KEY, users)

