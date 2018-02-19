""" Routes for developers """
from flask import Blueprint, url_for, render_template
from ovs import app
dev_home_page_bp = Blueprint('/', __name__,)


@dev_home_page_bp.route("/")
def dev_home_page():
    """ A home page that displays links to all accessible routes """
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods:
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links.remove('/')
    return render_template('dev_home_page.html', links=links)
