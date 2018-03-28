from sys import exit
from app import app,mysql,flask_login,login_manager
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

@login_dummy.route('/creds',methods=['POST'])
def login_new():
    s =  json.loads(request.data)
    print s
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
        return redirect('/home')
    else:
        return redirect('/login')


@login_dummy.route('/',methods=['GET'])
def login_new_one():
    if (flask_login.current_user.is_authenticated):
        return redirect('/home')
    return render_template('login2.html')


@login_manager.user_loader
def load_user(id):
    obj = User(username = "abhijay@tententen.in",password="abhijay",id=id)
    resp = obj.get_user_from_id()
    return resp

@login_manager.unauthorized_handler
def unauth_handler():
    return redirect("/login")

@login_dummy.route('/logout',methods=['GET'])
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect("/login")