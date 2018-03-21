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
