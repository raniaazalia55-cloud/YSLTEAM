from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from ..models.database import get_db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard.dashboard'))
    return render_template('login.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            db = get_db()
            cur = db.cursor()
            # TODO: Ganti dengan password hashing menggunakan werkzeug.security
            cur.execute(
                "SELECT * FROM user WHERE username = %s AND password = %s",
                (username, password)
            )
            user = cur.fetchone()
            cur.close()
            db.close()

            if user:
                session['username']  = user['username']
                session['user_name'] = user['user_name']
                session['role']      = user['role']
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Username atau Password salah!', 'danger')
        except Exception as e:
            flash(f'Database Error: {str(e)}', 'danger')

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
