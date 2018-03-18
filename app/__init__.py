from flask import Flask
from flask_mysqldb import MySQL
import flask_login
app =Flask(__name__)

from config import *

# updating mysql creds from config 
app.config.update(db_conf)
app.config.update(app_secret)
mysql = MySQL(app)


from controller import *

# initiating login manager

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
