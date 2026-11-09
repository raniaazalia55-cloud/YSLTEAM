import os
import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask


def create_app():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    app.config.from_object('config.Config')

    # Daftarkan semua Blueprint di dalam fungsi untuk menghindari circular import
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .repository.routes import repository_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(repository_bp)

    return app
