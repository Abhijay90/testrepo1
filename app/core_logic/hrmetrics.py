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

hrmetrics=Blueprint('hrmetrics',__name__)


#Cost
@homepage_dashboard.route('',methods=['GET'])
@user_access()
def dashboard(obj):
    resp = obj.employee_cost(json=0)
    return render_template('index.html',resp=resp["data"])
    
@hrmetrics.route('/',methods=['GET'])
@user_access()
def employee_cost(obj):
    resp = obj.user_averages_rs(required_field="Employee_Cost",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/revenue_employee',methods=['GET'])
@user_access()
def Revenue_Per_Employee(obj):
    resp = obj.user_averages_rs(required_field="Revenue_Per_Employe",json=0)
    resp["data"].update(dict(head="Revenue Per Employee ($)"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/employee_cost_to_revenue',methods=['GET'])
@user_access()
def Employee_Cost_Revenue_percentage(obj):
    resp = obj.user_averages_rs(required_field="Employee_Cost_Revenue_percentage",json=0)
    resp["data"].update(dict(head="Employee Cost as % of Revenue"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/employee_cost_avg',methods=['GET'])
@user_access()
def Average_Employee_Cost(obj):
    resp = obj.user_averages_rs(required_field="Average_Employee_Cost_rs",json=0)
    resp["data"].update(dict(head="Average Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])



# performance

@hrmetrics.route('/attrition_voluntary',methods=['GET'])
@user_access()
def Voluntary_Attrition_Annual(obj):
    resp = obj.user_averages_rs(required_field="Voluntary_Attrition_Annual",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])



@hrmetrics.route('/attrition_all',methods=['GET'])
@user_access()
def attrition_overall(obj):
    resp = obj.user_averages_rs(required_field="Overall_Attrition_Annual",json=0)
    resp["data"].update(dict(head="Employee Voluntary Attrition - Annual"))
    return render_template('benchmark_results.html',resp=resp["data"])



@hrmetrics.route('/hiring_quarterly',methods=['GET'])
@user_access()
def Average_Hiring_Quarterly(obj):
    resp = obj.user_averages_rs(required_field="Average_Hiring_Quarterly",json=0)
    resp["data"].update(dict(head="Average Hiring"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/hiring_annual',methods=['GET'])
@user_access()
def Average_Hiring_Annual(obj):
    resp = obj.user_averages_rs(required_field="Average_Hiring_Annual",json=0)
    resp["data"].update(dict(head="Average Hiring (Annual)"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/hiring_cost',methods=['GET'])
@user_access()
def Cost_Per_Hire_Annual(obj):
    resp = obj.user_averages_rs(required_field="Cost_Per_Hire_Annual",json=0)
    resp["data"].update(dict(head="Cost Per Hiring Annual"))
    return render_template('benchmark_results.html',resp=resp["data"])




@hrmetrics.route('/time_to_hire',methods=['GET'])
@user_access()
def Time_to_Hire_Days(obj):
    resp = obj.user_averages_rs(required_field="Time_to_Hire_Days",json=0)
    resp["data"].update(dict(head="Time to Hire (Days)"))
    return render_template('benchmark_results.html',resp=resp["data"])



# Efficiency

@hrmetrics.route('/headcount_hr',methods=['GET'])
@user_access()
def HR_Headcount(obj):
    resp = obj.user_averages_rs(required_field="HR_Headcount",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])

@hrmetrics.route('/employee_to_hr',methods=['GET'])
@user_access()
def Employee_to_HR(obj):
    resp = obj.user_averages_rs(required_field="Employee_to_HR",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])

@hrmetrics.route('/hr_bp_headcount',methods=['GET'])
@user_access()
def HR_BP_Headcount(obj):
    resp = obj.user_averages_rs(required_field="HR_BP_Headcount",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])

@hrmetrics.route('/ratio_employee_hrbp',methods=['GET'])
@user_access()
def Employee_HR_BP_Ratio(obj):
    resp = obj.user_averages_rs(required_field="Employee_HR_BP_Ratio",json=0)
    resp["data"].update(dict(head="Employee Cost (INR Crore or $)"))
    return render_template('benchmark_results.html',resp=resp["data"])


@hrmetrics.route('/aggregate_data',methods=['POST'])
@user_access()
def aggregate_data(obj):
    import json
    in_key =  json.loads(request.form['aggregate_key'])
    try:
        is_chro =  json.loads(request.form['is_chro'])
    except:
        is_chro=0
    # in_key=["Employee_HR_BP_Ratio","HR_BP_Headcount"]
    resp_data=[]
    for i in in_key:
        resp = obj.user_averages_rs(required_field=i,json=0,db=ger_resp_head(i)["db"],show_metric=ger_resp_head(i)["show_metric"])
        if resp["status"]:
            resp["data"].update(dict(head=ger_resp_head(i)["name"]))
            resp_data.append(dict(key=i,data=resp["data"]))
        else:
            return render_template('benchmark_results.html',resp=resp_data)
    # print resp_data
    # return response_json(data=resp_data,status=True,as_json=1)
    # return response_json(data={},status=True,as_json=1)
    if is_chro:
        return render_template('chro.html',resp=resp_data)
    else:
        return render_template('benchmark_results.html',resp=resp_data)

def ger_resp_head(key):
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

