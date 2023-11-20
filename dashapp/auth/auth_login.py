from flask import Flask
from .user import UserDAO
from flask_login import LoginManager

#### Flask-Login #####
# add flask-login module to flask app
def add_login_manager(app: Flask):
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id): #required by login manager
        user = UserDAO.get_user_by_id(user_id)
        return user

    @login_manager.unauthorized_handler
    def unauthorized():
        return "You are not allowed to access. Please contact HR OSP Team (@gavin.ma) to enable."

    return app     