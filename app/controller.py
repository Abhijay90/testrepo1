from app import app
from flask import jsonify,render_template,url_for,request,Response
from home.homepage import homepage_bp

# from flask_restful import Api

from app import mysql

# api = Api(app)
app.register_blueprint(homepage_bp,url_prefix='/')