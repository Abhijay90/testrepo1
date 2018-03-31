from app.db import db,db_cursor
from app.utility import response_json 
from functools import wraps

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

        return wraps(function)(__decorator)
        # return __decorator
    return decorator



class metrics_logic(object):
    def __init__(self,user_type=0):
        self.user_type=user_type
        self.user_access=""
        self.user_access_list=[]

    def user_accessible_fields(self):
        if session:
            self.user_type=int(session["data"]["user_type"])
            self.user_company_id=int(session["data"]["user_company_id"])
            self.user_id=int(session["user_id"])
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


    def to_string(self,val):
        for sub in val:
            for key in sub:
                sub[key] = str(sub[key])
        print val
        return val



    def __avg_data(self,selector,json=1):
        query = '''select AVG({selector}) as data from company_data where id <> {user_company_id};'''.format(selector =selector ,user_company_id=self.user_company_id)

        query_user_company='''select {selector} as data from company_data where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)
        try:
            resp = db(query,asdict=True)
            resp_user = db(query_user_company,asdict=True)
            if not resp:
                return response_json(data={},status=False,state=2)
            if not resp_user:
                return response_json(data={},status=False,state=2)
            res=dict(data=int(resp[0]["data"]),user_data = int(resp_user[0]["data"]))
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)

    def __avg_data_by_industry(self,selector,json=1):
        query = '''select truncate(AVG({selector}),2) as data from company_data where id <> {user_company_id};'''.format(selector =selector ,user_company_id=self.user_company_id)

        query_user_company='''select truncate({selector},2) as data,industry as name from company_data where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)
        try:
            # for json conversion
            resp = self.to_string(db(query,asdict=True))
            
            resp_user = self.to_string(db(query_user_company,asdict=True))

            if not resp:
                return response_json(data={},status=False,state=2)
            
            if not resp_user:
                return response_json(data={},status=False,state=2)
            
            ### getting avg data of industry
            query_user_industry = '''select truncate(AVG({selector}),2) as data, industry as name from company_data where id <> {user_company_id}  group by industry order by data desc limit 5;'''.format(selector =selector ,user_company_id=self.user_company_id)

            query_user_industry_drill_down = '''select truncate(AVG({selector}),2) as data, industry as name,tier as sub_name from company_data where id <> {user_company_id}  group by industry,tier order by data desc limit 5;'''.format(selector =selector ,user_company_id=self.user_company_id)


            resp_selector_tab = self.to_string(db(query_user_industry,asdict=True))

            resp_selector_tab_drill_down = self.to_string(db(query_user_industry_drill_down,asdict=True))

            
            if not resp_selector_tab:
                return response_json(data={},status=False,state=2)

            res=dict(data=resp[0]["data"],user_data = resp_user[0]["data"],tab_data = resp_selector_tab,drill_down = resp_selector_tab_drill_down)
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)


    def __avg_data_by_tier(self,selector,json=1):
        query_user_company='''select truncate({selector},2) as data,tier as name from company_data where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)
        

        try:
            resp_user = self.to_string(db(query_user_company,asdict=True))
            
            if not resp_user:
                return response_json(data={},status=False,state=2)
            ### getting avg of tier
            query_user_tier = '''select truncate(AVG({selector}),2) as data,tier as name from company_data where id <> {user_company_id} and tier <>"" and tier is not null group by tier;'''.format(selector =selector ,user_company_id=self.user_company_id,industry = resp_user[0]["name"])
            query_user_tier_drill_down = '''select truncate(AVG({selector}),2) as data,tier as name,industry as sub_name from company_data where id <> {user_company_id} and tier <>"" and tier is not null group by tier,industry;'''.format(selector =selector ,user_company_id=self.user_company_id,industry = resp_user[0]["name"])
            resp_selector_tab = self.to_string(db(query_user_tier,asdict=True))
            resp_selector_tab_drill_down = self.to_string(db(query_user_tier_drill_down,asdict=True))
            if not resp_selector_tab:
                return response_json(data={},status=False,state=2)

            res=dict(data=-1,user_data = resp_user[0]["data"],tab_data = resp_selector_tab,drill_down = resp_selector_tab_drill_down)
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)


    def __avg_data_by_revenue(self,selector,json=1):
        query_user_company='''select truncate({selector},2) as data, 
        case when Revenue_rs<500 then "<500 Cr"
        when Revenue_rs>500 and Revenue_rs<1000 then ">500 Cr and <1000 Cr"
        else  ">1000 Cr" end as name
        from company_data where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)

        query_user_revenue_bracket = '''select truncate(AVG(data),2) as data, name from  (select {selector} as data,
        case when Revenue_rs<500 then "<500 Cr"
        when Revenue_rs>500 and Revenue_rs<1000 then ">500 Cr and <1000 Cr"
        else  ">1000 Cr" end as name from company_data where id <> {user_company_id} ) a group by name;'''.format(selector =selector ,user_company_id=self.user_company_id)
        
        try:
            resp_user = self.to_string(db(query_user_company,asdict=True))
            if not resp_user:
                return response_json(data={},status=False,state=2)
            ### getting avg of tier
            resp_selector_tab = self.to_string(db(query_user_revenue_bracket,asdict=True))
            if not resp_selector_tab:
                return response_json(data={},status=False,state=2)

            res=dict(data=-1,user_data = resp_user[0]["data"],tab_data = resp_selector_tab,drill_down = [])
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)
        

    def user_averages_rs(self,required_field,json=1):
        if not self.is_function_accessible(required_field=required_field)["status"]:
            return response_json(data={},status=False,as_json=json)
        data=dict(tier={},industry={},peers=dict())
        tier = self.__avg_data_by_tier(selector=required_field,json=0)
        industry = self.__avg_data_by_industry(selector=required_field,json=0)
        peers = self.__avg_data_by_revenue(selector=required_field,json=0)
        if tier["status"] and industry["status"] and peers["status"]:
            data["tier"]=tier["data"]
            data["peers"]=peers["data"]
            data["industry"]=industry["data"]
            return response_json(data=data,status=True,as_json=json)
        return response_json(data={},status=False,as_json=json)

    def update_company_data(self,data,json=1):
        if not self.is_function_accessible(required_field="update")["status"]:
            return response_json(data={},status=False,as_json=json)
        query_str = '''user_id="{}",company_id="{}",'''.format(self.user_id,self.user_company_id)
        query_list=[]
        for i in data:
            key=i
            value=data[i]
            if value:
                query_list.append('''{}="{}"'''.format(key,value))
        query_str+=",".join(query_list )
        query  =  '''insert into user_data_log SET {};'''.format(query_str);
        try:
            db(query,commit=True)
        except:
            return response_json(data={},status=False,as_json=json)
        return response_json(data = {} , status=True,as_json=json)

        



    # def Approx_Indian_HeadCount_avg(self,json=1):
    #     if not self.is_function_accessible(required_field="Approx_India_Headcount")["status"]:
    #         return response_json(data={},status=False,as_json=json)
    #     return self.__avg_data(selector="Approx_India_Headcount",json=json)

    # def employee_cost(self,json=1):
    #     if not self.is_function_accessible(required_field="Employee_Cost")["status"]:
    #         return response_json(data={},status=False,as_json=json)
    #     return self.__avg_data_by_revenue(selector="Employee_Cost",json=json)

    # def Employee_Cost():
