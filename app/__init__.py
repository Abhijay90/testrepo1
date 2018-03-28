from flask import Flask
from flask_mysqldb import MySQL
import flask_login
from flask_sqlalchemy import SQLAlchemy
app =Flask(__name__)

from config import *

# updating mysql creds from config 
app.config.update(db_conf)
app.config.update(app_secret)
mysql = MySQL(app)

# sql alchemy init
app.config.update(db_conf_alchemy)
alchemy_db = SQLAlchemy(app)


# initiating login manager

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


from controller import *