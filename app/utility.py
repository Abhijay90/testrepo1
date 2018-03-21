try:
    import json
except:
    print "install json"
    exit(0)

try:
    from flask import Response
except:
     print "install flask"
     exit(0)

from decimal import Decimal

def response_json(data,status,state=0,as_json=1):
    response_data={"status":False,"state":0,"data":{}}
    response_data["status"] = status
    response_data["state"] = state
    response_data["data"] = data
    # print response_data
    if not as_json:
        return response_data
    return Response(json.dumps(response_data,default=defaultencode),mimetype='application/json')


def defaultencode(o):
    if isinstance(o, Decimal):
        # Subclass float with custom repr?
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)
