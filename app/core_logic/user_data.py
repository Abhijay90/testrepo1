from app.db import db,db_cursor
from app.utility import response_json 

try:
    from flask import session
except:
     print "install flask"
     exit(0)

class UserData():


    def __init__(self,user_id=0):
        print session
        if user_id:
            self.user_id=user_id
        else:
            self.user_id=int(session["user_id"])

        print self.user_id

    def profile(self,json):
        query = '''select a.name,b.name as company_name,a.phone,a.email from auth_user a inner join company_data b on a.company=b.id where a.id={user_id}; '''.format(user_id =self.user_id)
        # print query
        order_of_data=["name","company_name","email","phone"]
        try:
            res={}
            resp = db(query,asdict=True)
            if resp:
                res.update({"data":resp[0]})
            res.update({"key_order":order_of_data})
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)
