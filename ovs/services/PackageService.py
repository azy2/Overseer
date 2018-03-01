
from ovs import app
from ovs.models.UserModel import User
from ovs.models.PackageModel import Package
from ovs.services import UserService
db = app.database.instance()


class PackageService:
    @staticmethod
    def create_package(user_id, checked_by, checked_at, description):
        new_package = Package(user_id=user_id, checked_by=checked_by, checked_at=checked_at, description=description)
        db.add(new_package)
        db.commit()
        return new_package
