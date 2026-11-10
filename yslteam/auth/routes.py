from flask import render_template, session, redirect, url_for, flash
from . import dashboard_bp

@dashboard_bp.route('/dashboard')
def index():
    # Proteksi halaman: Wajib login terlebih dahulu
    if 'username' not in session:
        flash('Silakan login terlebih dahulu untuk mengakses dashboard.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Ambil data user dari session
    username = session.get('username')
    role = session.get('role', 'User')

    return render_template('dashboard.html', username=username, role=role)