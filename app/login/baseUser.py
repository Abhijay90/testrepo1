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

from app import flask_login#,alchemy_db
from app import alchemy_db
from app.db import db,db_cursor


from flask import session


'''
CREATE TABLE `auth_user` (
  `id` int(11) auto_increment,
  `name` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `role` varchar(255) DEFAULT NULL,
  `department` varchar(255) DEFAULT NULL,
  `Revenue` int(11) DEFAULT NULL,
  `employees` int(11) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `is_active` int(11) DEFAULT '1',
  `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_type` int(11) default 1,
  PRIMARY KEY (`id`)
);
'''

class User(alchemy_db.Model):
    __tablename__ = "auth_user"
    id = alchemy_db.Column('id',alchemy_db.Integer, primary_key = True)
    username = alchemy_db.Column('email',alchemy_db.String(255))
    password = alchemy_db.Column('password',alchemy_db.String(255))
    name=alchemy_db.Column('name',alchemy_db.String(255))
    role = alchemy_db.Column('role',alchemy_db.String(255))
    department = alchemy_db.Column('department',alchemy_db.Integer)
    employees = alchemy_db.Column('employees',alchemy_db.Integer)
    phone = alchemy_db.Column('phone',alchemy_db.String(255))
    is_active = alchemy_db.Column('is_active',alchemy_db.String(255))
    user_type = alchemy_db.Column('user_type',alchemy_db.Integer)
    user_company_id = alchemy_db.Column('company',alchemy_db.Integer)


    def __init__(self ,username,password,id,active=True):
        self.id = id
        self.username = username
        self.password = password
        self.active = active

    def get_user_from_id(self):
        return self.query.filter_by(id=self.id).first()

    def get_id(self):
        return unicode(self.id)
        

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def __password(self):
        return self.password

    def is_unique(self):
        query='''select * from auth_user where email like "{email}" '''.format(email=self.username)
        res = db(query,asdict=True)
        if not res:
            return dict(status=True)
        return dict(status=False)

    def __set_session_vars(self,user_row):
        session["data"]={"user_company_id":user_row.user_company_id,"user_type":user_row.user_type}


    def insert_user_in_db(self,name,company,role,department,revenue,employees,phone):
        #use orm here, doing with raw query to make it work first
        s = self.is_unique["status"]
        if not s["status"]:
            return s

        query='''insert into auth_user(name,company,role,department,revenue,employees,phone,email,password,is_active) values({name},{company},{role},{department},{revenue},{employees},{phone},{email},{password},1)'''.fromat(name=name,company=company,role=role,department=department,revenue=revenue,employees=employees,phone=phone,email=self.username,password=password)
        self.id = db(query,commit=True,lastrowid=True)
        return self.id

    def login(self):
        registered_user = self.query.filter_by(username=self.username,password=self.__password()).first()
        if registered_user is None:
            return dict(status=False,data=dict())
        flask_login.login_user(registered_user)
        self.__set_session_vars(registered_user)
        return dict(status=True,data=dict(id=registered_user.id,user_type=registered_user.user_type,user_company_id=registered_user.user_company_id))
   


