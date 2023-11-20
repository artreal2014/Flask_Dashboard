import requests
import logging
from flask import render_template, session, redirect, url_for #, jsonify, request

from .user import UserDAO
from flask_login import login_user, logout_user, current_user

# const
# open api capability
USER_ACCESS_TOKEN_URI = "/open-apis/authen/v1/access_token"
APP_ACCESS_TOKEN_URI = "/open-apis/auth/v3/app_access_token/internal"
USER_INFO_URI = "/open-apis/authen/v1/user_info"

# const
# The session key required to store user info in the session
USER_INFO_KEY = "UserInfo"

## Lark level authentication 

class Auth(object):
    def __init__(self, lark_host, app_id, app_secret):
        self.lark_host = lark_host
        self.app_id = app_id
        self.app_secret = app_secret
        self._app_access_token = ""
        self._user_access_token = ""
        
    @property
    def user_access_token(self):
        return self._user_access_token
      
    @property
    def app_access_token(self):
        return self._app_access_token
      
    # You can also get user_info here.
    # However, considering that the user_access_token is required by multiple APIs  on the server-side,
    # you should get the user_access_token before you get user_info.
    # please remember to refresh the user_access_token according to the openplatform document
    def authorize_user_access_token(self, code):
        # The method for getting the user_access_token, is implemented based on the open capabilities of Lark. 
        self.authorize_app_access_token()
        url = self._gen_url(USER_ACCESS_TOKEN_URI)
        # "app_access_token" is in the HTTP request header
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.app_access_token,
        }
        # The temporary authorization code is in the HTTP request body
        req_body = {"grant_type": "authorization_code", "code": code}
        response = requests.post(url=url, headers=headers, json=req_body)
        Auth._check_error_response(response)
        self._user_access_token = response.json().get("data").get("access_token")
        
    def get_user_info(self):
        # The method of getting user info, is implemented based on the open capabilities of Lark.
        url = self._gen_url(USER_INFO_URI)
        # "user_access_token" is in the HTTP request header
        headers = {
            "Authorization": "Bearer " + self.user_access_token,
            "Content-Type": "application/json",
        }
        response = requests.get(url=url, headers=headers)
        Auth._check_error_response(response)
        # For the descriptions of fields in the response body and examples, please see the Open Platform document
        return response.json().get("data")
      
    def authorize_app_access_token(self):
        # The method of getting the app_access_token, is implemented based on the open capabilities of Lark.
        url = self._gen_url(APP_ACCESS_TOKEN_URI)
        # "app_id" and "app_secret" are in the HTTP request body
        req_body = {"app_id": self.app_id, "app_secret": self.app_secret}
        response = requests.post(url, req_body)
        Auth._check_error_response(response)
        self._app_access_token = response.json().get("app_access_token")
        
    def _gen_url(self, uri):
        # Join the Lark Open Platform domain lark_host and uri.
        return "{}{}".format(self.lark_host, uri)
      
    @staticmethod
    def _check_error_response(resp):
        # Check whether the response body contains error messages
        # check if the response contains error information
        if resp.status_code != 200:
            raise resp.raise_for_status()
        response_dict = resp.json()
        code = response_dict.get("code", -1)
        if code != 0:
            logging.error(response_dict)
            raise LarkException(code=code, msg=response_dict.get("msg"))

class LarkException(Exception):
    # Process and display the error code and error message returned from Lark
    def __init__(self, code=0, msg=None):
        self.code = code
        self.msg = msg
        
    def __str__(self) -> str:
        return "{}:{}".format(self.code, self.msg)
    __repr__ = __str__

# Business logic
class Biz(object):
    @staticmethod
    def home_handler():
        #1. if user id is in the list, redirect. else，go to user account html page
        #print (url_for('/dashboard/'))
        user_info = session[USER_INFO_KEY]
        user_id = user_info['user_id']
        user = UserDAO.get_user_by_id(user_id) #lookup userid from db/excel config

        if user is not None:
            login_user(user) # flask-login, login in the user
            logging.info(f"User {user_id} login successfully.")
            return redirect(url_for('/dashboard/'))
        else:
            logging.warning(f"User {user_id} not found in the user list.")
            return render_template("err_info.html", err_info="You are not allowed to access. Please request access from HR System Team")

    @staticmethod
    def login_handler():
        # The auto-login process is required.
        return render_template("index.html", user_info={"name": "unknown"}, login_info="needLogin")

    @staticmethod
    def login_failed_handler(err_info):
        # The homepage loading process after an error occurs
        return Biz._show_err_info(err_info)
    
    # Session in Flask has a concept very similar to that of a cookie, 
    # i.e. data containing identifier to recognize the computer on the network, 
    # except the fact that session data is stored in a server.
    @staticmethod
    def _show_user_info():
        # Directly display the user information stored in the session
        return render_template("index.html", user_info=session[USER_INFO_KEY], login_info="alreadyLogin")
    
    @staticmethod
    def _show_err_info(err_info):
        # Display error messages on the page.
        return render_template("err_info.html", err_info=err_info)
