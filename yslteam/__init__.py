from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'yslteam-secret-key-2026')

    # Impor Blueprint tepat di dalam function agar bebas circular import
    from yslteam.auth.routes import auth_bp
    from yslteam.dashboard.routes import dashboard_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    return app