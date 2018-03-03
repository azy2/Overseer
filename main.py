# from ovs import app
# from ovs import routes
# from ovs.services import UserService
# from ovs.utils import roles

# if __name__ == '__main__':
#     app.register_blueprint(routes.UserRoutes, url_prefix='/user')
#     app.register_blueprint(routes.AdminRoutes, url_prefix='/admin')
#     app.register_blueprint(routes.ManagerRoutes, url_prefix='/manager')
#     app.register_blueprint(routes.AuthRoutes, url_prefix='/auth')
#     app.register_blueprint(routes.DevRoutes, url_prefix='/')

#     super_user = UserService.get_user_by_email(app.config['SUPERUSER']['email']).one_or_none()
#     if not super_user:
#         UserService.create_user(app.config['SUPERUSER']['email'],
#                                 app.config['SUPERUSER']['first_name'],
#                                 app.config['SUPERUSER']['last_name'],
#                                 roles.ADMIN,
#                                 app.config['SUPERUSER']['password'])

#     host = '0.0.0.0' if app.config['DEVELOPMENT'] else '127.0.0.1'
#     app.run(host=host, port=app.config['PORT'], debug=app.config['DEVELOPMENT'])


from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()