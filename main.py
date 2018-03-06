from ovs import app
from ovs import routes
from ovs.services import UserService
from ovs.utils import roles

app.register_blueprint(routes.OvsRoutes, url_prefix='/')
app.register_blueprint(routes.AdminRoutes, url_prefix='/admin')
app.register_blueprint(routes.ManagerRoutes, url_prefix='/manager')
app.register_blueprint(routes.ResidentRoutes, url_prefix='/resident')
app.register_blueprint(routes.AuthRoutes, url_prefix='/auth')
app.register_blueprint(routes.DevRoutes, url_prefix='/dev')

super_user = UserService.get_user_by_email(
    app.config['SUPERUSER']['email']).one_or_none()
if not super_user:
    UserService.create_user(app.config['SUPERUSER']['email'],
                            app.config['SUPERUSER']['first_name'],
                            app.config['SUPERUSER']['last_name'],
                            roles.ADMIN,
                            app.config['SUPERUSER']['password'])
if app.config['APP_ENV'] == 'DEV':
    resident_user = UserService.get_user_by_email(
        app.config['RESIDENT']['email']).one_or_none()
    if not resident_user:
        UserService.create_user(app.config['RESIDENT']['email'],
                                app.config['RESIDENT']['first_name'],
                                app.config['RESIDENT']['last_name'],
                                roles.RESIDENT,
                                app.config['RESIDENT']['password'])
