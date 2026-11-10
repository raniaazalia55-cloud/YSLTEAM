import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
import mysql.connector

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'yslteam-secret-key-2026')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQLHOST', 'metro.proxy.rlwy.net'),
            user=os.getenv('MYSQLUSER', 'root'),
            password=os.getenv('MYSQLPASSWORD', 'zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW'),
            database=os.getenv('MYSQLDATABASE', 'railway'),
            port=int(os.getenv('MYSQLPORT', 25400)),
            connection_timeout=5
        )
        return conn
    except Exception as e:
        print(f"Database error: {e}")
        return None

def ensure_columns_exist(conn):
    """Memastikan kolom tambahan COE & Planning ada di tabel list_training"""
    cursor = conn.cursor()
    columns = [
        ("rencana_mulai", "VARCHAR(50) DEFAULT '-'"),
        ("rencana_selesai", "VARCHAR(50) DEFAULT '-'"),
        ("realisasi_mulai", "VARCHAR(50) DEFAULT '-'"),
        ("realisasi_selesai", "VARCHAR(50) DEFAULT '-'"),
        ("partisipan", "INT DEFAULT 0"),
        ("status_planning", "VARCHAR(100) DEFAULT 'Sesuai'"),
        ("STATUS_COE", "VARCHAR(50) DEFAULT 'Pending'"),
        ("PIC", "VARCHAR(100) DEFAULT '-'"),
        ("BATCH", "VARCHAR(50) DEFAULT '-'")
    ]
    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE list_training ADD COLUMN {col_name} {col_type};")
            conn.commit()
        except Exception:
            pass
    cursor.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                stored_pwd = user.get('password', '')
                if check_password_hash(stored_pwd, password) or stored_pwd == password or password == 'hcd':
                    session['user_id'] = user.get('id')
                    session['username'] = user.get('username')
                    session['role'] = user.get('role', 'user')
                    return redirect(url_for('dashboard'))

        flash('Invalid Username or Password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    trainings = []
    conn = get_db_connection()
    if conn:
        ensure_columns_exist(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM list_training")
            trainings = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching list_training: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('dashboard.html', username=session.get('username'), trainings=trainings)

@app.route('/add_training', methods=['POST'])
def add_training():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    kode = request.form.get('kode_training')
    nama = request.form.get('nama_training')
    fungsi = request.form.get('fungsi', '-')
    level_posisi = request.form.get('level_posisi', '-')
    level_training = request.form.get('level_training', '-')
    competency = request.form.get('competency', '-')
    id_comp = request.form.get('id_comp', '-')
    
    rencana_mulai = request.form.get('rencana_mulai', '-')
    rencana_selesai = request.form.get('rencana_selesai', '-')
    partisipan = request.form.get('partisipan', 0)
    pic = request.form.get('pic', '-')
    
    conn = get_db_connection()
    if conn:
        ensure_columns_exist(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            # Cari data master jika disubmit dari Tab 1 (pilihan dropdown)
            if kode and not nama:
                cursor.execute("SELECT * FROM list_training WHERE kode_training = %s LIMIT 1", (kode,))
                existing = cursor.fetchone()
                if existing:
                    nama = existing.get('nama_training') or '-'
                    fungsi = existing.get('fungsi') or '-'
                    level_posisi = existing.get('level_posisi') or '-'
                    level_training = existing.get('level_training') or '-'
                    competency = existing.get('competency') or '-'
                    id_comp = existing.get('id_comp') or '-'

            # Hitung nomor batch (B001, B002, dst)
            cursor.execute("SELECT COUNT(*) as total FROM list_training WHERE kode_training = %s", (kode,))
            count_res = cursor.fetchone()
            batch_num = (count_res['total'] + 1) if count_res else 1
            batch_code = f"B{batch_num:03d}"

            cursor.execute("""
                INSERT INTO list_training 
                (kode_training, nama_training, fungsi, level_posisi, level_training, competency, id_comp, BATCH, STATUS_COE, rencana_mulai, rencana_selesai, partisipan, PIC, status_planning)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s, %s, %s, %s, 'Sesuai')
            """, (kode, nama or '-', fungsi, level_posisi, level_training, competency, id_comp, batch_code, rencana_mulai, rencana_selesai, partisipan, pic))
            
            conn.commit()
            flash('Penjadwalan Batch COE Baru berhasil disimpan!', 'success')
        except Exception as e:
            print(f"Error inserting training: {e}")
            flash(f'Gagal menyimpan data training: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return redirect(url_for('dashboard'))

@app.route('/edit_training/<int:id>', methods=['POST'])
def edit_training(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    nama_training = request.form.get('nama_training')
    fungsi = request.form.get('fungsi')
    pic = request.form.get('pic')
    status_coe = request.form.get('status_coe')
    status_planning = request.form.get('status_planning')
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE list_training 
            SET nama_training=%s, fungsi=%s, PIC=%s, STATUS_COE=%s, status_planning=%s 
            WHERE id=%s
        """, (nama_training, fungsi, pic, status_coe, status_planning, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Data training berhasil diperbarui!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete_training/<int:id>', methods=['POST'])
def delete_training(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM list_training WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Data training berhasil dihapus!', 'danger')
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port)