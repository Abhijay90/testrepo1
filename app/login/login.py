from sys import exit
from app import app,mysql,flask_login
from flask import redirect,url_for
from functools import wraps
from app.db import db,db_cursor

from app.utility import response_json 

from app.login.baseUser import User
try:
    from flask import Blueprint, render_template,jsonify,request,Response,session,make_response
except:
     print "install flask"
     exit(0)

try:
    import json
except:
    print "install json"
    exit(0)

logging_in = Blueprint('login',__name__)#,template_folder='templates')

login_dummy = Blueprint('login_dummy',__name__)

@logging_in.route('/new',methods=['POST'])
def login_new():
    s =  json.loads(request.data)
    try:
        username = s["username"]
        if not username:
            return response_json(status=False,data=dict(msg="enter username"))
    except:
        return response_json(status=False,data=dict(msg="enter username"))
    try:
        secret = s["password"]
        if not secret:
            return response_json(status=False,data=dict(msg="enter password"))
    except:
        return response_json(status=False,data=dict(msg="enter password"))

    obj = User(username = username,password=password,id=0)

    data = obj.login()

    if data["status"]:
        return obj.set_cookie(response_json(status=True,data={}),user_type=data["data"]["user_type"],user_company_id=data["data"]["user_company_id"]) #login
    else:
        return obj.set_cookie(response_json(status=False,data={}))



@login_dummy.route('/new',methods=['GET'])
def login_new_one():
    return render_template('login2.html')

@login_dummy.route('/',methods=['GET'])
def dummy_session():
    obj = User(username = "",password="",id=1)

    # obj.set_cookie(response_json(status=True,data={},as_json=1),user_type=1,user_company_id=1)
    return obj.set_cookie(make_response(render_template('login1.html')),user_type=1,user_company_id=1)
    # return redirect("/home", code=302)