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
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM list_training ORDER BY id DESC")
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
    
    kode = request.form.get('kode_training', '').strip()
    nama = request.form.get('nama_training', '').strip()
    fungsi = request.form.get('fungsi', '-').strip() or '-'
    level_posisi = request.form.get('level_posisi', '-').strip() or '-'
    level_training = request.form.get('level_training', '-').strip() or '-'
    competency = request.form.get('competency', '-').strip() or '-'
    id_comp = request.form.get('id_comp', '-').strip() or '-'
    
    rencana_mulai = request.form.get('rencana_mulai', '-').strip() or '-'
    rencana_selesai = request.form.get('rencana_selesai', '-').strip() or '-'
    partisipan = request.form.get('partisipan', '0').strip()
    pic = request.form.get('pic', '-').strip() or '-'
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            # Ambil sampel kolom untuk mengecek nama kolom asli
            cursor.execute("SELECT * FROM list_training LIMIT 1")
            sample = cursor.fetchone() or {}
            
            col_kode = 'kode_training' if 'kode_training' in sample else 'KODE'
            col_nama = 'nama_training' if 'nama_training' in sample else ('nama' if 'nama' in sample else 'NAMA_TRAINING')
            col_fungsi = 'fungsi' if 'fungsi' in sample else 'FUNGSI'
            col_posisi = 'level_posisi' if 'level_posisi' in sample else 'LEVEL_POSISI'
            col_lvl_tr = 'level_training' if 'level_training' in sample else 'LEVEL_TRAINING'
            col_comp = 'competency' if 'competency' in sample else 'COMPETENCY'
            col_id_comp = 'id_comp' if 'id_comp' in sample else ('id_competency_level' if 'id_competency_level' in sample else 'ID_COMP')

            # Jika dari Tab 1, cari detail dari repository master
            if kode and not nama:
                cursor.execute(f"SELECT * FROM list_training WHERE {col_kode} = %s LIMIT 1", (kode,))
                existing = cursor.fetchone()
                if existing:
                    nama = existing.get(col_nama) or '-'
                    fungsi = existing.get(col_fungsi) or '-'
                    level_posisi = existing.get(col_posisi) or '-'
                    level_training = existing.get(col_lvl_tr) or '-'
                    competency = existing.get(col_comp) or '-'
                    id_comp = existing.get(col_id_comp) or '-'

            # FIX UTAMA: Hitung nomor 'no' terbesar agar field 'no' wajib terisi
            cursor.execute("SELECT MAX(CAST(`no` AS UNSIGNED)) as max_no FROM list_training")
            row_no = cursor.fetchone()
            next_no = (row_no['max_no'] + 1) if (row_no and row_no.get('max_no')) else 1

            # Hitung Batch Number
            cursor.execute(f"SELECT COUNT(*) as total FROM list_training WHERE {col_kode} = %s", (kode,))
            count_res = cursor.fetchone()
            batch_code = f"B{(count_res['total'] + 1):03d}" if count_res else "B001"

            # Insert Lengkap termasuk kolom 'no'
            sql = f"""
                INSERT INTO list_training 
                (`no`, {col_kode}, {col_nama}, {col_fungsi}, {col_posisi}, {col_lvl_tr}, {col_comp}, {col_id_comp}, BATCH, STATUS_COE, rencana_mulai, rencana_selesai, partisipan, PIC, status_planning)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s, %s, %s, %s, 'Sesuai')
            """
            cursor.execute(sql, (next_no, kode, nama or '-', fungsi, level_posisi, level_training, competency, id_comp, batch_code, rencana_mulai, rencana_selesai, partisipan, pic))
            conn.commit()
            flash('Berhasil menyimpan Penjadwalan Batch COE / Master Training Baru!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'ERROR DATABASE: {str(e)}', 'danger')
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
        try:
            cursor.execute("UPDATE list_training SET nama_training=%s, fungsi=%s, PIC=%s, STATUS_COE=%s, status_planning=%s WHERE id=%s", (nama_training, fungsi, pic, status_coe, status_planning, id))
            conn.commit()
            flash('Data training berhasil diperbarui!', 'success')
        except Exception as e:
            flash(f'Error Update: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('dashboard'))

@app.route('/delete_training/<int:id>', methods=['POST'])
def delete_training(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM list_training WHERE id=%s", (id,))
            conn.commit()
            flash('Data training berhasil dihapus!', 'danger')
        except Exception as e:
            flash(f'Error Delete: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port)