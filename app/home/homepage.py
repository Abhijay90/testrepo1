from sys import exit
from app import mysql,login_manager,flask_login

from app.utility import response_json 

try:
    from flask import Blueprint, render_template,jsonify,request,Response,session,redirect
except:
     print "install flask"
     exit(0)

from app.db import db,db_cursor
import datetime
 
homepage_bp = Blueprint('homepage',__name__,template_folder='templates')
user_check= Blueprint('multicheck',__name__,template_folder='templates')

@homepage_bp.route('',methods=['GET'])
@flask_login.login_required
def homepage():
    return render_template('home.html',resp=session["data"])


@user_check.route('',methods=['GET'])
@flask_login.login_required
def multicheck():
    return render_template('index_choice.html',resp=session["data"])

@user_check.route('/workforce',methods=['GET'])
@flask_login.login_required
def workforce_index():
    return render_template('index_choice_workforce.html')
