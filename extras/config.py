db_conf = {'MYSQL_HOST':'localhost',
'MYSQL_USER': 'root',
'MYSQL_PASSWORD': 'root',
'MYSQL_DB': "testing",
'MYSQL_PORT': 3306,
'MYSQL_UNIX_SOCKET': None,
'MYSQL_CONNECT_TIMEOUT': 10,
'MYSQL_READ_DEFAULT_FILE': None,
'MYSQL_USE_UNICODE':True,
'MYSQL_CHARSET':'utf8',
'MYSQL_SQL_MODE':None,
'MYSQL_CURSORCLASS':None}

db_conf_alchemy = {'SQLALCHEMY_DATABASE_URI':'mysql://root:root@localhost/testing',
'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

app_secret={"SECRET_KEY":"LSho3t1qIf5pPIvbGVtl"}
