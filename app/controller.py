from app import app
from flask import jsonify,render_template,url_for,request,Response
from home.homepage import homepage_bp,user_check
from login.login import user_login,user_logout
from core_logic.hrmetrics import homepage_dashboard,hrmetrics
from core_logic.profile import user_profile
from core_logic.user_input import user_input

# from flask_restful import Api

from app import mysql

# api = Api(app)
app.register_blueprint(user_profile,url_prefix='/profile')
app.register_blueprint(user_input,url_prefix='/user_data')
app.register_blueprint(homepage_bp,url_prefix='/home')
app.register_blueprint(user_login,url_prefix='/')
app.register_blueprint(user_logout,url_prefix='/logout')
app.register_blueprint(homepage_dashboard,url_prefix='/dashboard')
app.register_blueprint(user_check,url_prefix='/user_options')
app.register_blueprint(hrmetrics,url_prefix='/metrics')


# app.register_blueprint(logging_in,url_prefix = '/login/')
