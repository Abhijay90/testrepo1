from app import app
import sys
import os
if __name__ == '__main__':
    s = os.getcwd()
    print s
    sys.path.append(s+"/app")
    app.debug = True
    app.run(host='0.0.0.0',threaded=True)

