from app import mysql

def _dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    s =[
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    return s

def db(query,commit=0,asdict=0):
    conn = mysql.connection
    cur = conn.cursor()
    try:
        cur.execute(query)
        if commit:
            conn.commit()
    except:
        print "error"
        return []
    if asdict:
        return _dictfetchall(cur)
    return cur.fetchall()

def db_cursor():
    conn = mysql.connection
    cur = conn.cursor()
    return conn,cur
