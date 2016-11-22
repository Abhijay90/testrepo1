from flask import Flask
from flask_mysqldb import MySQL
# from flask.ext import login
app =Flask(__name__)
mysql = MySQL(app)
from config import *
from controller import *
