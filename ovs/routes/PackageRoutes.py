
from flask import Blueprint
from ovs.services import PackageService
packages_bp = Blueprint('package', __name__,)


@packages_bp.route('/add', methods=['POST'])
def add_package():
    return PackageService.create_package()
