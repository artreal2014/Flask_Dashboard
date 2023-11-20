
import pandas as pd
from flask_login import UserMixin  
from dotenv import load_dotenv, find_dotenv
import os 
load_dotenv(find_dotenv())
USERSOURCE_DIR = os.getenv("USERSOURCE_DIR")

#basic user model 
class User (UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username  
        self.role = role
#        self.is_authenticated = False #required 

#user model data access, for db or file based storage 
class UserDAO:
    # static variables
    file_path = f"{USERSOURCE_DIR}/config_users.xlsx"
    users = []  #static variable

    @classmethod
    def init_users(cls):
        if len(cls.users)==0:
            df_users = pd.read_excel(cls.file_path)
            for idx, row in df_users.iterrows():
                user = User(
                    id = row['id'], 
                    username = row['name'], 
                    role = row['role']
                )
                cls.users.append(user) #build user list
        else:
            pass 

    #reload file
    @classmethod
    def reload_users(cls):
        df_users = pd.read_excel(cls.file_path)
        cls.users = [] #reset
        for idx, row in df_users.iterrows():
            user = User(
                id = row['id'], 
                username = row['name'], 
                role = row['role']
            )
            cls.users.append(user) #build user list

    #return User model
    @classmethod
    def get_user_by_id(cls, user_id):
        for u in cls.users:
            if u.id == user_id:
                return u
        return None #can't found, return None

    #set authenticated by user id
    @classmethod
    def authenticate_user_by_id(cls, user_id):
        for u in cls.users:
            if u.id == user_id:
                u.is_authenticated = True

UserDAO.init_users() #static user list
#for u in UserDAO.users:
#    print (u.is_authenticated)
#    print (u.role)