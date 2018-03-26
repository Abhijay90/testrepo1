from app.db import db,db_cursor

try:
    from flask import session
except:
     print "install flask"
     exit(0)

class CRUD_operation():
    def __init__(self):
        self.user_id=session["data"]["user_id"]
        
    def __create_record(self):
        pass

    def __edit_record(self):
        pass

    def __delete_record(self):
        pass

    def __add_property(self):
        pass

    def __remove_property(self):
        pass

    def __get_product(self):
        pass




