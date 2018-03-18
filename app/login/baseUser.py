'''
Registration elements:

Name
company
role
department
Revenue
employees
email
phone,
password,
is_active
'''

from app import flask_login
from app.db import db,db_cursor

from flask import session

class User(flask_login.UserMixin):
    def __init__(self , username , password , id , active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_id(self):
        return self.id

    def is_active(self):
        return self.active


    def get_auth_token(self):
        return make_secure_token(self.username , key='secret_key')

    def is_unique(self):
        query='''select * from auth_user where email like "{email}" '''.format(email=self.username)
        res = db(query,asdict=True)
        if not res:
            return dict(status=True)
        return dict(status=False)


    def insert_user_in_db(self,name,company,role,department,revenue,employees,phone):
        #use orm here, doing with raw query to make it work first
        s = self.is_unique["status"]
        if not s["status"]:
            return s

        query='''insert into auth_user(name,company,role,department,revenue,employees,phone,email,password,is_active) values({name},{company},{role},{department},{revenue},{employees},{phone},{email},{password},1)'''.fromat(name=name,company=company,role=role,department=department,revenue=revenue,employees=employees,phone=phone,email=self.username,password=password)
        self.id = db(query,commit=True,lastrowid=True)
        return self.id

    def set_cookie(self,response,user_type=0,user_company_id=0):
        values = dict(user_id=self.id,user_type=user_type,user_company_id=user_company_id)
        session['data'] = values
        values= "random_val" # session key , do session properly
        response.set_cookie('temp',value=values)
        return response

    def login(self):
        resp=dict(status=True,val=dict(user_type=1,user_company_id=1))
        return resp
