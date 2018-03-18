from app.db import db,db_cursor
from app.utility import response_json 

try:
    from flask import session
except:
     print "install flask"
     exit(0)


def user_access(required_field="",redirect="/"):
    def decorator(function):
        def __decorator(*args, **kwargs):
            obj = metrics_logic()
            resp = obj.user_accessible_fields()
            if not resp["status"]:
                return dict(status=False)

            if not obj.is_function_accessible(required_field)["status"]:
                return dict(status=False)
            kwargs.update({"obj":obj})
            return function(*args, **kwargs)
        return __decorator
    return decorator



class metrics_logic(object):
    def __init__(self,user_type=0):
        self.user_type=user_type
        self.user_access=""
        self.user_access_list=[]

    def user_accessible_fields(self,):
        if session:
            self.user_type=int(session["data"]["user_type"])
            self.user_company_id=int(session["data"]["user_company_id"])
        if not self.user_type:
            return dict(status=False)
        query_user_access = '''select fields from user_roles where user_type={user_type};'''.format(user_type=int(self.user_type))
       
        try: 
            resp_user_access_fields=db(query_user_access,asdict=True)
            if resp_user_access_fields:
                self.user_access_list=[i["fields"] for i in resp_user_access_fields]
                self.user_access=",".join(self.user_access_list)
                return dict(status=True,data=self.user_access_list)
        except Exception as e:
            return dict(status=False)

    def is_function_accessible(self,required_field):
        if not required_field:
            return dict(status=True)
        if (self.user_access=="*") or (required_field in self.user_access_list):
            return dict(status=True)
        return dict(status=False)


    def __avg_data(self,selector,json=1):
        query = '''select AVG({selector}) as data from company_data_master where id <> {user_company_id};'''.format(selector =selector ,user_company_id=self.user_company_id)

        query_user_company='''select {selector} as data from company_data_master where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)
        try:
            resp = db(query,asdict=True)
            resp_user = db(query_user_company,asdict=True)
            if not resp:
                return response_json(val={},status=False,state=2)
            if not resp_user:
                return response_json(val={},status=False,state=2)
            res=dict(data=int(resp[0]["data"]),user_data = int(resp_user[0]["data"]))
        except Exception as e:
            print e
            if json:
                return response_json(val={},status=False)
            else:
                return dict(val={},status=False)
        if json:
            return response_json(val=res,status=True)
        else:
            return dict(val=res,status=True)


    def Approx_Indian_HeadCount_avg(self,json=1):
        if not self.is_function_accessible(required_field="Approx_India_Headcount")["status"]:
            if json:
                return response_json(val={},status=False)
        return self.__avg_data(selector="Approx_India_Headcount",json=json)

    # def Employee_Cost():
