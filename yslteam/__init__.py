import os
from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    
    # Load konfigurasi utama
    app.config.from_object(Config)
    
    # Konfigurasi Koneksi MySQL Railway
    app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'mysql.railway.internal')
    app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW')
    app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'railway')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))

    # Import & Registrasi Blueprint
    from yslteam.auth.routes import auth_bp
    from yslteam.dashboard.routes import dashboard_bp
    from yslteam.repository.routes import repository_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repository_bp)

    return app