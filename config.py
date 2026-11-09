import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'integrated_ipd_secret_2026')
    
    MYSQL_HOST = os.getenv('MYSQLHOST', 'mysql.railway.internal')
    MYSQL_USER = os.getenv('MYSQLUSER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
    MYSQL_DB = os.getenv('MYSQLDATABASE', 'railway')
    MYSQL_PORT = int(os.getenv('MYSQLPORT', 3306))
    
    # Alias untuk pemanggilan variabel singkat
    MYSQLHOST = MYSQL_HOST
    MYSQLUSER = MYSQL_USER
    MYSQLPASSWORD = MYSQL_PASSWORD
    MYSQLDATABASE = MYSQL_DB
    MYSQLPORT = MYSQL_PORT