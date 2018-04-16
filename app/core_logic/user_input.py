from sys import exit
from app.utility import response_json 
from app import app,flask_login,login_manager

try:
    from flask import Blueprint, render_template,jsonify,request,Response,session,redirect
except:
     print "install flask"
     exit(0)

from app.db import db,db_cursor
import datetime

from app.core_logic.metrics import user_access
 

user_input = Blueprint('user_input',__name__)


@user_input .route('/',methods=['GET'])
@flask_login.login_required
def user_data():
    # obj = UserData()
    # resp = obj.profile(json=0)
    pg_val=0
    try:
        pg_val = int(request.args["workforce"])
    except:
        pass

    if not pg_val:
        return render_template('enter_metrics.html')
    else:
        return render_template('enter_metrics_workforce.html')

@user_input .route('/',methods=['POST'])
@flask_login.login_required
@user_access()
def user_data_post(obj):
	import json
	in_key =  json.loads(request.form['aggregate_key'])
	resp = obj.update_company_data(in_key,json=0)
	return redirect('/home')
    # return render_template('login.html',resp=resp["data"])