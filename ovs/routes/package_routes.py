# IS THIS FILE USED ANYWHERE??? <-- !!!
from flask import Blueprint
from ovs.services import UserService
from ovs.services import PackageService
from ovs.forms import PackageForm
packages_bp = Blueprint('package', __name__,)


@packages_bp.route('/add', methods=['POST'])
def add_package():
    form = PackageForm(csrf_enabled=False)
    email = form.email.data
    description = form.description.data
    user = UserService.get_user_by_email(email).first()
    user_id = user.id

    return PackageService.create_package().json()
