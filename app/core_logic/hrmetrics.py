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

from app.core_logic.metrics import user_access
 
homepage_dashboard = Blueprint('dashboard',__name__)

hrmetrics=Blueprint('metrics',__name__)

@homepage_dashboard.route('',methods=['GET'])
@user_access()
def dashboard(obj):
    resp = obj.employee_cost(json=0)
    return render_template('index.html',resp=resp["data"])
    
@hrmetrics.route('',methods=['GET'])
@user_access()
def employee_cost(obj):
    resp = obj.user_averages_rs(required_field="Employee_Cost",json=0)
    return render_template('index.html',resp=resp["data"])


# @hrmetrics.route('/revenue_employee',methods=['GET'])
# @user_access()
# def Revenue_Per_Employe(obj):
#     resp = obj.user_averages_rs(required_field="Revenue_Per_Employe",json=0)
#     return render_template('index.html',resp=resp["data"])



@homepage_dashboard.route('',methods=['GET'])
def api_people_count():
    user_type=0
    if session:
        user_type=int(session["data"]["user_type"])
        user_company_id=int(session["data"]["user_company_id"])
    if not user_type:
        return response_json(data={},status=False)

    query_user_access = '''select group_concat(fields) as fields from user_roles where user_type={user_type};'''.format(user_type=int(user_type))
    query = '''select {fields} from company_data_master limit 10;'''

    try:
        resp_user_access_fields=db(query_user_access,asdict=True)
        if resp_user_access_fields:
            res = db(query.format(fields=resp_user_access_fields[0]["fields"]),asdict=True)
            if not res:
                return response_json(data={},status=False,state=2)
        else:
            return response_json(data={},status=False,state=2)
    except Exception as e:
        return response_json(data={},status=False)
    if not res:
        return response_json(data={},status=False)
    return response_json(data=res,status=True)


