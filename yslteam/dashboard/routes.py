from flask import render_template, session, redirect, url_for, flash
from . import dashboard_bp

@dashboard_bp.route('/dashboard')
def index():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('auth.login'))
    
    return render_template('dashboard.html', username=session.get('username'), role=session.get('role', 'User'))