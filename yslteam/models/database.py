import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        # Utamakan variabel dari Railway Environment Variables
        host = os.getenv('MYSQLHOST', 'metro.proxy.rlwy.net')
        user = os.getenv('MYSQLUSER', 'root')
        password = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
        database = os.getenv('MYSQLDATABASE', 'railway')
        port = int(os.getenv('MYSQLPORT', 25400))

        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connection_timeout=5  # Mencegah Gunicorn crash/hang saat booting
        )
        return conn
    except Error as e:
        print(f"[DATABASE ERROR] Gagal terhubung ke MySQL: {e}")
        return None