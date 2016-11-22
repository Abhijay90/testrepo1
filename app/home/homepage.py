from sys import exit
from app import mysql

try:
    from flask import Blueprint, render_template,jsonify,request,Response
except:
     print "install flask"
     exit(0)
try:
    import json
except:
    print "install json"
    exit(0)

from app.db import db,db_cursor
import datetime
 
homepage_bp = Blueprint('homepage',__name__)

@homepage_bp.route('',methods=['GET'])
def homepage():
    query = '''select 1 as tm;'''
    try:
        res = db(query,asdict=True)
    except Exception as e:
        print e
        return Response(json.dumps({'response':{'status':'failure'}}),  mimetype='application/json')
    if not res:
        return Response(json.dumps({'response':{'status':'failure'}}),  mimetype='application/json')

    return Response(json.dumps({'response':{'status':'success'},'data':res[0]['tm']}),  mimetype='application/json')