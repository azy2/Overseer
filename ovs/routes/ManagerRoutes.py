
from flask import Blueprint, render_template, request
from ovs.services import ManagerService

manager_bp = Blueprint('manager', __name__,)


@manager_bp.route('/manage_residents', methods=['GET'])
def manage_residents():
	return render_template('manager/manage_residents.html')
