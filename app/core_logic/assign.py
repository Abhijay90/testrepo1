from sys import exit
from app import mysql

try:
    from flask import Blueprint, render_template,jsonify,request,Response,session
except:
     print "install flask"
     exit(0)

from app.db import db,db_cursor
import datetime

 = Blueprint('dashboard',__name__)


# def edit_data():
    