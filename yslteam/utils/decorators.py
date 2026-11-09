from functools import wraps
from flask import session, redirect, url_for, jsonify


def login_required(f):
    """Decorator: redirect ke login jika user belum autentikasi."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def hcd_required(f):
    """Decorator: tolak akses jika role bukan HCD (untuk endpoint API)."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'HCD':
            return jsonify({'success': False, 'message': 'Akses Ditolak: Hanya HCD Specialist yang diperbolehkan.'}), 403
        return f(*args, **kwargs)
    return decorated
