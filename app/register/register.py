'''
Registration elements:

Name
company
role
department
Revenue
employees
email
phone'''


try:
    from flask import Blueprint,request,Response,jsonify, abort
except:
     print "install flask"
     exit(0)

from app.login.baseUser import User
from app.utility import response_json 

register = Blueprint('register',__name__)#,template_folder='templates')

@register.route('/metrics/',methods = ['POST'])
def register():
    s =  json.loads(request.data)
    name = s["name"]
    company = s["org_name"]
    role = s["role"]
    department = s["department"]
    revenue = s["revenue"]
    employees = s["employees"]
    email = s["email"]
    phone = s["phone"]
    password=s["password"]


    obj = User(username = email,password=password,id=0)
    resp = obj.insert_user_in_db(name,company,role,department,revenue,employees,phone) # registration happening here
    if resp:
        if obj.login()["status"]:
            return obj.set_cookie(response_json(status=True,val={})) #login
        else:
            return response_json(status=False,val={})
    else:
        return response_json(status=False,val={})





