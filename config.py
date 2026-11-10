import os
from urllib.parse import urlparse

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'integrated_ipd_secret_2026')
    
    # 1. Cek jika Railway menyediakan MYSQL_URL atau DATABASE_URL lengkap
    db_url = os.getenv('MYSQL_URL') or os.getenv('DATABASE_URL')
    if db_url:
        parsed = urlparse(db_url)
        MYSQL_HOST = parsed.hostname or 'localhost'
        MYSQL_PORT = parsed.port or 3306
        MYSQL_USER = parsed.username or 'root'
        MYSQL_PASSWORD = parsed.password or ''
        MYSQL_DB = parsed.path.lstrip('/') or 'railway'
    else:
        # 2. Mendukung format Railway (tanpa underscore) dan standar (dengan underscore)
        MYSQL_HOST = os.getenv('MYSQLHOST') or os.getenv('MYSQL_HOST') or 'mysql.railway.internal'
        MYSQL_PORT = int(os.getenv('MYSQLPORT') or os.getenv('MYSQL_PORT') or 3306)
        MYSQL_USER = os.getenv('MYSQLUSER') or os.getenv('MYSQL_USER') or 'root'
        MYSQL_PASSWORD = os.getenv('MYSQLPASSWORD') or os.getenv('MYSQL_PASSWORD') or 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW'
        MYSQL_DB = os.getenv('MYSQLDATABASE') or os.getenv('MYSQL_DB') or 'railway'
    
    # Alias untuk kompatibilitas
    MYSQLHOST = MYSQL_HOST
    MYSQLUSER = MYSQL_USER
    MYSQLPASSWORD = MYSQL_PASSWORD
    MYSQLDATABASE = MYSQL_DB
    MYSQLPORT = MYSQL_PORT
