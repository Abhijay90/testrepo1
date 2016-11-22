from app import app
from flask import jsonify,render_template,url_for,request,Response
from home.homepage import homepage_bp

from app import mysql

app.register_blueprint(homepage_bp,url_prefix='/')

