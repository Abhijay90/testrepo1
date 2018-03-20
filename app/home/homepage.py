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
    query = '''select 1 as tm;'''
    try:
        res = db(query,asdict=True)
    except Exception as e:
        return response_json(val={},status=False)
    if not res:
        return response_json(val={},status=False)
    # return render_template('index.html')
    return response_json(val=res[0]['tm'],status=True)


@user_check.route('',methods=['GET'])
def multicheck():
    return render_template('index_choice.html')
    # return response_json(val=res[0]['tm'],status=True)
