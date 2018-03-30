from sys import exit
from app.utility import response_json 
from app import app,flask_login,login_manager

try:
    from flask import Blueprint, render_template,jsonify,request,Response,session
except:
     print "install flask"
     exit(0)

from app.db import db,db_cursor
import datetime

from app.core_logic.user_data import UserData
 

user_profile = Blueprint('profile',__name__)


@user_profile .route('/',methods=['GET'])
@flask_login.login_required
def user_data():
    obj = UserData()
    resp = obj.profile(json=0)
    print resp
    return render_template('profile.html',resp=resp["data"] )