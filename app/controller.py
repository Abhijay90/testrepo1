from app import app
from flask import jsonify,render_template,url_for,request,Response
from home.homepage import homepage_bp,user_check
from login.login import login_dummy
from core_logic.hrmetrics import homepage_dashboard,hrmetrics
# from flask_restful import Api

from app import mysql

# api = Api(app)
app.register_blueprint(homepage_bp,url_prefix='/')
app.register_blueprint(login_dummy,url_prefix='/login/')
app.register_blueprint(homepage_dashboard,url_prefix='/dashboard')
app.register_blueprint(user_check,url_prefix='/user_options')
app.register_blueprint(hrmetrics,url_prefix='/metrics')

# app.register_blueprint(logging_in,url_prefix = '/login/')
