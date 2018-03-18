try:
    import json
except:
    print "install json"
    exit(0)

try:
    from flask import Blueprint, render_template,jsonify,request,Response
except:
     print "install flask"
     exit(0)


def response_json(val,status,state=0):
	response_data={"status":False,"state":0,"data":{}}
	response_data["status"]=status
	response_data["state"]=state
	response_data["data"]=val
	return Response(json.dumps(response_data),mimetype='application/json')
