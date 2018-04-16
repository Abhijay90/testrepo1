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
        return val

    def __avg_data_by_industry(self,selector,json=1):
        query = '''select truncate(AVG({selector}),2) as data from company_data where id <> {user_company_id};'''.format(selector =selector ,user_company_id=self.user_company_id)

        query_user_company='''select truncate({selector},2) as data,
            case when industry = "Software / Internet" then "IT Services"
            when industry = "Computers - Software" then "IT Services"
            else industry end 
            as name from company_data where id = {user_company_id}; '''.format(selector=selector,user_company_id=self.user_company_id)
        
        try:
            # for json conversion
            resp = self.to_string(db(query,asdict=True))
            
            resp_user = self.to_string(db(query_user_company,asdict=True))

            if not resp:
                return response_json(data={},status=False,state=2)
            
            if not resp_user:
                return response_json(data={},status=False,state=2)
            
            ### getting avg data of industry
            query_user_industry = '''select truncate(AVG({selector}),2) as data, 
                case when industry = "Software / Internet" then "IT Services"
                when industry = "Computers - Software" then "IT Services"
                else industry end  
                as name from company_data where id <> {user_company_id} and {selector}<>0  group by industry order by data desc limit 5;'''.format(selector =selector ,user_company_id=self.user_company_id)

            query_user_industry_drill_down = '''select truncate(AVG({selector}),2) as data, 
                case when industry = "Software / Internet" then "IT Services"
                when industry = "Computers - Software" then "IT Services"
                else industry end  
                as name,tier as sub_name from company_data where id <> {user_company_id} and {selector}<>0  group by industry,tier order by data desc limit 5;'''.format(selector =selector ,user_company_id=self.user_company_id)


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
            query_user_tier = '''select truncate(AVG({selector}),2) as data,tier as name from company_data where id <> {user_company_id} and tier <>"" and tier is not null and {selector}<>0 group by tier;'''.format(selector =selector ,user_company_id=self.user_company_id,industry = resp_user[0]["name"])
            query_user_tier_drill_down = '''select truncate(AVG({selector}),2) as data,tier as name,
                case when industry = "Software / Internet" then "IT Services"
                when industry = "Computers - Software" then "IT Services"
                else industry end  
                as sub_name from company_data where id <> {user_company_id} and tier <>"" and tier is not null and {selector}<>0 group by tier,industry;'''.format(selector =selector ,user_company_id=self.user_company_id,industry = resp_user[0]["name"])
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
        else  ">1000 Cr" end as name from company_data where id <> {user_company_id} and {selector}<>0) a group by name;'''.format(selector =selector ,user_company_id=self.user_company_id)
        
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

    def __avg_data(self,selector,json=1):
        query_data_india='''select truncate(AVG({selector}),2) as data,"Tier I (India)" as name from company_extended_data where {selector}<>0 and company_international=0; '''.format(selector=selector)

        query_data_int='''select truncate(AVG({selector}),2) as data,"Tier I (India+MNC)" as name from company_extended_data where {selector}<>0 ; '''.format(selector=selector)

        try:
            resp_user = self.to_string(db(query_data_india,asdict=True))
            
            if not resp_user:
                return response_json(data={},status=False,state=2)

            data  = db(query_data_int,asdict=True) 
            data.append(resp_user[0])
            resp_selector_tab = self.to_string(data)

            # print resp_selector_tab
            resp_selector_tab_drill_down=[]
            if not resp_selector_tab:
                return response_json(data={},status=False,state=2)
            
            res=dict(data=-1,user_data = -1,tab_data = resp_selector_tab,drill_down = resp_selector_tab_drill_down)
        except Exception as e:
            print e
            return response_json(data={},status=False,as_json=json)
        return response_json(data=res,status=True,as_json=json)
        

    def user_averages_rs(self,required_field,db,show_metric,json=1):
        if not self.is_function_accessible(required_field=required_field)["status"]:
            return response_json(data={},status=False,as_json=json)
        data=dict(tier={},industry={},peers={})
        for i in self.__show_metric(show_metric):
            if i=="tier":
                tier = self.__avg_data_by_tier(selector=required_field,json=0)
                if tier["status"]:
                    data["tier"]=tier["data"]
                else:
                    return response_json(data={},status=False,as_json=json)
            if i=="industry":
                industry = self.__avg_data_by_industry(selector=required_field,json=0)
                if industry["status"]:
                    data["industry"]=industry["data"]
                else:
                    return response_json(data={},status=False,as_json=json)
            if i=="peers":
                peers = self.__avg_data_by_revenue(selector=required_field,json=0)
                if peers["status"]:
                    data["peers"]=peers["data"]
                else:
                    return response_json(data={},status=False,as_json=json)

            if i=="single_tier":
                tier = self.__avg_data(selector=required_field,json=0)
                if tier["status"]:
                    data["tier"]=tier["data"]
                else:
                    return response_json(data={},status=False,as_json=json)
        return response_json(data=data,status=True,as_json=json)
            
    def update_company_data(self,data ,json=1):
        if not self.is_function_accessible(required_field="update")["status"]:
            return response_json(data={},status=False,as_json=json)
        query_str = '''user_id="{}",company_id="{}",'''.format(self.user_id,self.user_company_id)
        query_list=[]
        __db = "company_data"
        for i in data:
            key=i
            value=data[i]
            __db=self.__ger_resp_head(i)["db"]
            if value:
                query_list.append('''{}="{}"'''.format(key,value))
        query_str+=",".join(query_list )
        query_update='''update {} set {} where id = {};''' .format(__db,",".join(query_list ),self.user_company_id)
        query  =  '''insert into user_data_log SET {};'''.format(query_str);
        try:
            db(query,commit=True)
            db(query_update,commit=True)
        except:
            return response_json(data={},status=False,as_json=json)
        return response_json(data = {} , status=True,as_json=json)

    def __show_metric(self,value):
        if value==0:
            return ["tier","industry","peers"]
        if value==1:
            return ["single_tier"]

    
    def __ger_resp_head(self,key):
        headings={
        "Employee_HR_BP_Ratio":{"name":"Employee/HR Business Partner","db":"company_data","show_metric":0},
        # "HR_BP_Headcount":"Employee Cost($)",
        "Employee_to_HR":{"name":"Employee to HR Ratio","db":"company_data","show_metric":0},
        "HR_Headcount":{"name":"HR Headcount","db":"company_data","show_metric":0},
        "Time_to_Hire_Days":{"name":"Time to Hire (Days)","db":"company_data","show_metric":0},
        "Cost_Per_Hire_Annual":{"name":"Cost Per Hiring Annual($)","db":"company_data","show_metric":0},
        "Average_Hiring_Annual":{"name":"Gross Hiring (Annual)","db":"company_data","show_metric":0},
        "Average_Hiring_Quarterly":{"name":"Gross Hiring (Quarterly)","db":"company_data","show_metric":0},
        "Overall_Attrition_Annual":{"name":"Overall Attrition (Annual)","db":"company_data","show_metric":0},
        "Voluntary_Attrition_Annual":{"name":"Voluntary Attrition (Annual)","db":"","show_metric":0},
        "Employee_Cost":{"name":"Average Employee Cost ($)","db":"company_data","show_metric":0},
        "Revenue_Per_Employe":{"name":"Revenue Per Employee ($)","db":"company_data","show_metric":0},
        "Employee_Cost_Revenue_percentage":{"name":"Employee Cost as % of Revenue","db":"company_data","show_metric":0},
        "Average_Employee_Cost_rs":{"name":"Avg. Employee Cost (Lakh Rs.)","db":"company_data","show_metric":0},
        "Training_Spend_Annual":{"name":"Training Spend (Annual)","db":"company_data","show_metric":0},
        "Training_Spend_Revenue_Percentage":{"name":"Training Spend as % of Revenue","db":"company_data","show_metric":0},
        "Training_Spend_Per_Person":{"name":"Training Spend Per Person ($)","db":"company_data","show_metric":0},
        "overall_revenue_growth":{"name":"Overall Revenue Growth(%)","db":"company_extended_data","show_metric":1},
        "headcount_growth":{"name":"Headcount Growth (%)","db":"company_extended_data","show_metric":1},
        "ebit":{"name":"EBIT (%)","db":"company_extended_data","show_metric":1},
        "percentage_headcount":{"name":"Headcount in Tier II & Tier III","db":"company_extended_data","show_metric":1},
        "campus_hire":{"name":"Campus Hires 2017 (%)","db":"company_extended_data","show_metric":1},
        "time_to_bill":{"name":"Time to Bill (Days)","db":"company_extended_data","show_metric":1},
        "bench_percentage":{"name":"Bench Strength (%)","db":"company_extended_data","show_metric":1},
        "utilization_overall":{"name":"Utilisations Overall (%)","db":"company_extended_data","show_metric":1},
        "utilization_lateral":{"name":"Utilisations Lateral (%)","db":"company_extended_data","show_metric":1},
        "employee_cost_revenue_percentage":{"name":"Employee Cost as a % of Revenues","db":"company_extended_data","show_metric":1}
        }

        return headings[key]





    # def Approx_Indian_HeadCount_avg(self,json=1):
    #     if not self.is_function_accessible(required_field="Approx_India_Headcount")["status"]:
    #         return response_json(data={},status=False,as_json=json)
    #     return self.__avg_data(selector="Approx_India_Headcount",json=json)

    # def employee_cost(self,json=1):
    #     if not self.is_function_accessible(required_field="Employee_Cost")["status"]:
    #         return response_json(data={},status=False,as_json=json)
    #     return self.__avg_data_by_revenue(selector="Employee_Cost",json=json)

    # def Employee_Cost():
