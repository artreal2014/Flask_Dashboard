#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import logging
from flask import Flask, redirect
from app.auth.routes import auth_bp
from app.auth.auth_login import add_login_manager
#from app.dash.routes import dash_bp

# log format settings
LOG_FORMAT = "%(asctime)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)

# The secret_key is required if you want to use the flask session
SECRET_KEY = "ThisIsSecretKey"

def init_app():
    # Initialize the flask web application
    app = Flask(
        __name__, 
        static_url_path="/public", static_folder="public",
        template_folder="templates"
    )
    app.secret_key = SECRET_KEY
    app.debug = True

    #lark auth
    app.register_blueprint(auth_bp)
    #flask-login auth 
    app=add_login_manager(app)

    #root -> auth
    @app.route("/")
    def auth():
        return redirect('/auth')

    # add dashboards
    from .dashapp.dashboard import add_dashboard
    app = add_dashboard(app) #add turnover dash to app    

    return app