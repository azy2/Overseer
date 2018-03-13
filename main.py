import os
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

if os.environ.get("WERKZEUG_RUN_MAIN") == 'true':
    user = UserService.get_user_by_email(
        app.config[roles.ADMIN]['email']).one_or_none()
    if not user:
        UserService.create_user(app.config[roles.ADMIN]['email'],
                                app.config[roles.ADMIN]['first_name'],
                                app.config[roles.ADMIN]['last_name'],
                                roles.ADMIN,
                                app.config[roles.ADMIN]['password'])
    if app.config['TESTING'] or app.config['DEVELOPMENT']:
        for user_role in [roles.RESIDENT, roles.RESIDENT_ADVISOR, roles.STAFF,
                          roles.OFFICE_MANAGER, roles.BUILDING_MANAGER]:
            user = UserService.get_user_by_email(
                app.config[user_role]['email']).one_or_none()
            if not user:
                UserService.create_user(app.config[user_role]['email'],
                                        app.config[user_role]['first_name'],
                                        app.config[user_role]['last_name'],
                                        user_role,
                                        app.config[user_role]['password'])
