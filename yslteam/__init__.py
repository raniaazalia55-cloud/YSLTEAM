import os
from flask import Flask
from flask_mysqldb import MySQL  # atau connector yang kamu pakai
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Load konfigurasi dari class Config
    app.config.from_object(Config)
    
    # Backup / Fallback langsung jika env vars di Railway tidak terbaca
    app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'mysql.railway.internal')
    app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
    app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'railway')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

    # Inisialisasi blueprint dan extension lain di bawahnya...
    
    return app