from services.admin_service import AdminService
from database import JsonDatabase
import dotenv


class AdminServiceImpl(AdminService):
    def __init__(self):
        self.password = dotenv.get_key("env/.env", "PASSWORD")
        self.database = JsonDatabase("json_data/admins.json")

    def authorize(self, password: str, user: str) -> bool:
        if self.password == password:
            self.database.info = self.database.info["Data"] + [user]
            return True
        else:
            print("incorrect password.")
            return False

    def check_admin(self, user: str) -> bool:
        pass


admin_service = AdminServiceImpl()
admin_service.authorize("admin123", 123456)
admin_service.authorize("admin13", 123456)
