""" Routes for developers """
from flask import Blueprint, url_for, render_template
from ovs import app
from ovs.utils.roles import UserRole
dev_bp = Blueprint('/dev', __name__,)


def has_no_empty_params(rule):
    """ Checks if the rule is valid for navigation """
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@dev_bp.route("/")
def dev_home_page():
    """ A home page that displays links to all accessible routes """
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)

    links.remove('/')
    return render_template('dev_home_page.html', links=links)
