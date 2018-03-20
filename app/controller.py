from app import app
from flask import jsonify,render_template,url_for,request,Response
from home.homepage import homepage_bp
from login.login import login_dummy
from core_logic.hrmetrics import homepage_dashboard
# from flask_restful import Api

from app import mysql

# api = Api(app)
app.register_blueprint(homepage_bp,url_prefix='/home')
app.register_blueprint(login_dummy,url_prefix='/login/')
app.register_blueprint(homepage_dashboard,url_prefix='/dashboard')
# app.register_blueprint(logging_in,url_prefix = '/login/')
