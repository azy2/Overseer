import os
from ovs import app
from ovs import routes
from ovs.services import UserService
from ovs.utils import roles
from ovs import DataGen

app.register_blueprint(routes.OvsRoutes, url_prefix='/')
app.register_blueprint(routes.AdminRoutes, url_prefix='/admin')
app.register_blueprint(routes.ManagerRoutes, url_prefix='/manager')
app.register_blueprint(routes.ResidentRoutes, url_prefix='/resident')
app.register_blueprint(routes.AuthRoutes, url_prefix='/auth')
app.register_blueprint(routes.DevRoutes, url_prefix='/dev')

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    DataGen.create_defaults()
