
from ovs import app
from ovs.models.UserModel import User
from ovs.models.PackageModel import Package
from ovs.services import UserService
db = app.database.instance()


class PackageService:

    @staticmethod
    def create_package(user_id, checked_by, checked_at, ):
        pass
