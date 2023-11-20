
from flask import Blueprint, session, request, jsonify
from .auth import *
from dotenv import load_dotenv, find_dotenv
import os 

# Load environment variable parameters in the .env file
load_dotenv(find_dotenv())
# from .env
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
LARK_HOST = os.getenv("LARK_HOST")

#blue print for lark authentication
auth_bp = Blueprint( 'auth_bp', __name__, 
    template_folder='templates', static_folder='static', 
    url_prefix='/auth'
)
# Initialize auto-login process Auth with environment variables.
auth = Auth(LARK_HOST, APP_ID, APP_SECRET)

# When an error occurs, the page loading process "Biz.login_failed_handler(err_info)" is required.
@auth_bp.errorhandler(Exception)
def auth_error_handler(ex):
    return Biz.login_failed_handler(ex)

# Default homepage path
@auth_bp.route("/", methods=["GET"])
def get_home():
    # The first function to execute when the web app is opened
    # If no user info is stored in session, the auto-login process "Biz.login_handler()" is required.
    if USER_INFO_KEY not in session:
        logging.info("need to get user information")
        return Biz.login_handler() #eventually render template
    else:
        # If user info is stored in the session, directly use the page loading process "Biz.home_handler()".
        logging.info("already have user information")
        return Biz.home_handler() #eventually render template
    
@auth_bp.route("/callback", methods=["GET"])
def callback():
    # Get user info.
    # Get Codetransferred from the front-end.
    code = request.args.get("code")
    # Get the user_access_token first
    auth.authorize_user_access_token(code)
    # And then get user info.
    user_info = auth.get_user_info()
    # Store user info in the session.
    session[USER_INFO_KEY] = user_info
    return jsonify(user_info)

@auth_bp.route("/get_appid", methods=["GET"])
def get_appid():
    # Get the appid.
    # For security, do not disclose the app_id  and never write it in plaintext on the front-end. Therefore, this parameter is transferred from the server-side.
    return jsonify(
        {
            "appid": APP_ID
        }
    )
