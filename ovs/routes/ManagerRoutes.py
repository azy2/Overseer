
from flask import Blueprint, render_template, request
from ovs.services import ManagerService

manager_bp = Blueprint('manager', __name__,)


@manager_bp.route('/manage_residents', methods=['GET', 'POST'])
def manage_residents():
    """
    /manager/manage_residents severs a HTML with list of residents with their info.
    It will also be a link there to add/edit/delete residents with form inputs.
    """
    if request.method == 'GET':
        return render_template('manager/manage_residents.html')
    elif request.method == 'POST':
        pass

