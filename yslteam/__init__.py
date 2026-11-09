import os
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Load konfigurasi dari Config class
    app.config.from_object(Config)
    
    # Enforce variabel koneksi MySQL Railway
    app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'mysql.railway.internal')
    app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
    app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'railway')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

    # Register blueprint bawaan kamu
    try:
        from yslteam.auth.routes import auth_bp
        app.register_blueprint(auth_bp)
    except Exception:
        pass

    try:
        from yslteam.dashboard.routes import dashboard_bp
        app.register_blueprint(dashboard_bp)
    except Exception:
        pass

    try:
        from yslteam.repository.routes import repository_bp
        app.register_blueprint(repository_bp)
    except Exception:
        pass

    return app