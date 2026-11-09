import os

MYSQL_HOST = os.getenv('MYSQLHOST', 'mysql.railway.internal')
MYSQL_USER = os.getenv('MYSQLUSER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
MYSQL_DB = os.getenv('MYSQLDATABASE', 'railway')
MYSQL_PORT = int(os.getenv('MYSQLPORT', 3306))