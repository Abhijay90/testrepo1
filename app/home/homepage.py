from sys import exit
from app import mysql

from app.utility import response_json 

try:
    from flask import Blueprint, render_template,jsonify,request,Response,session
except:
     print "install flask"
     exit(0)

from app.db import db,db_cursor
import datetime
 
homepage_bp = Blueprint('homepage',__name__,template_folder='templates')
user_check= Blueprint('multicheck',__name__,template_folder='templates')

@homepage_bp.route('',methods=['GET'])
def homepage():
    return render_template('home.html')


@user_check.route('',methods=['GET'])
def multicheck():
    return render_template('index_choice.html')
