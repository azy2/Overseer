""" Routes under / """
from flask import Blueprint, render_template
ovs_bp = Blueprint('/', __name__,)


@ovs_bp.route('/')
def landing_page():
    """ Example route that generates a random user """
    return render_template('index.html')
