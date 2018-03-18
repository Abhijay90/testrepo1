from flask import Flask
from flask_mysqldb import MySQL
# from flask.ext import login
app =Flask(__name__)
from config import *
app.config.update(db_conf)
mysql = MySQL(app)
from controller import *
