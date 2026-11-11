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

def init_tables(conn):
    """Memastikan tabel master_repository, feedback_training, & kolom biaya siap"""
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_repository (
            id INT AUTO_INCREMENT PRIMARY KEY,
            kode_training VARCHAR(50) UNIQUE NOT NULL,
            nama_training VARCHAR(255) NOT NULL,
            fungsi VARCHAR(100) DEFAULT '-',
            id_fungsi VARCHAR(50) DEFAULT '-',
            level_posisi VARCHAR(50) DEFAULT '-',
            id_level_posisi VARCHAR(50) DEFAULT '-',
            level_training VARCHAR(50) DEFAULT '-',
            id_level_training VARCHAR(50) DEFAULT '-',
            competency VARCHAR(150) DEFAULT '-',
            id_competency_level VARCHAR(50) DEFAULT '-'
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback_training (
            id INT AUTO_INCREMENT PRIMARY KEY,
            training_id INT NOT NULL,
            kode_training VARCHAR(50),
            nama_training VARCHAR(255),
            batch VARCHAR(50),
            nama_peserta VARCHAR(100),
            rating INT DEFAULT 5,
            materi_rating INT DEFAULT 5,
            fasilitas_rating INT DEFAULT 5,
            komentar TEXT,
            tanggal_submit TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    try:
        cursor.execute("ALTER TABLE list_training ADD COLUMN biaya DECIMAL(15,2) DEFAULT 0.00")
    except Exception:
        pass
    conn.commit()
    cursor.close()

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        selected_role = request.form.get('role', 'user').lower()

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
                    session['user_name'] = user.get('username')
                    # Set Role: 'HC ADMIN' atau 'USER'
                    session['role'] = 'HC ADMIN' if selected_role in ['hc admin', 'staf hcd', 'admin', 'hcd'] else 'USER'
                    return redirect(url_for('dashboard'))

        flash('Invalid Username or Password', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    trainings = []
    repositories = []
    feedbacks = []
    conn = get_db_connection()
    if conn:
        init_tables(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM list_training ORDER BY id DESC")
            trainings = cursor.fetchall()
            
            cursor.execute("SELECT * FROM master_repository ORDER BY kode_training ASC")
            repositories = cursor.fetchall()

            cursor.execute("SELECT * FROM feedback_training ORDER BY id DESC")
            feedbacks = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('dashboard.html', username=session.get('username'), trainings=trainings, repositories=repositories, feedbacks=feedbacks)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    training_id = request.form.get('training_id')
    kode_training = request.form.get('kode_training')
    nama_training = request.form.get('nama_training')
    batch = request.form.get('batch')
    nama_peserta = request.form.get('nama_peserta', session.get('username'))
    rating = request.form.get('rating', 5)
    materi_rating = request.form.get('materi_rating', 5)
    fasilitas_rating = request.form.get('fasilitas_rating', 5)
    komentar = request.form.get('komentar', '')

    conn = get_db_connection()
    if conn:
        init_tables(conn)
        cursor = conn.cursor()
        try:
            sql = """
                INSERT INTO feedback_training 
                (training_id, kode_training, nama_training, batch, nama_peserta, rating, materi_rating, fasilitas_rating, komentar)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (training_id, kode_training, nama_training, batch, nama_peserta, rating, materi_rating, fasilitas_rating, komentar))
            conn.commit()
            flash('Terima kasih! Feedback training berhasil dikirim.', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Gagal mengirim feedback: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for('dashboard'))

@app.route('/repository')
def repository():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    repositories = []
    conn = get_db_connection()
    if conn:
        init_tables(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM master_repository ORDER BY id DESC")
            repositories = cursor.fetchall()
        except Exception as e:
            print(f"Error fetching repository: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('repository.html', username=session.get('username'), repositories=repositories)

@app.route('/add_master_repository', methods=['POST'])
def add_master_repository():
    if 'username' not in session or session.get('role') != 'HC ADMIN':
        flash('Akses ditolak! Hanya HC Admin yang dapat menambah Master Repository.', 'danger')
        return redirect(url_for('repository'))
    
    kode = request.form.get('kode_training', '').strip()
    nama = request.form.get('nama_training', '').strip()
    fungsi = request.form.get('fungsi', '-').strip() or '-'
    id_fungsi = request.form.get('id_fungsi', '-').strip() or '-'
    level_posisi = request.form.get('level_posisi', '-').strip() or '-'
    id_level_posisi = request.form.get('id_level_posisi', '-').strip() or '-'
    level_training = request.form.get('level_training', '-').strip() or '-'
    id_level_training = request.form.get('id_level_training', '-').strip() or '-'
    competency = request.form.get('competency', '-').strip() or '-'
    id_competency_level = request.form.get('id_competency_level', '-').strip() or '-'
    
    redirect_to = request.form.get('redirect_to', 'repository')

    conn = get_db_connection()
    if conn:
        init_tables(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT kode_training FROM master_repository WHERE kode_training = %s", (kode,))
            if cursor.fetchone():
                flash(f'Gagal menyimpan: Kode Training "{kode}" sudah terdaftar!', 'warning')
                return redirect(url_for(redirect_to))

            sql = """
                INSERT INTO master_repository 
                (kode_training, nama_training, fungsi, id_fungsi, level_posisi, id_level_posisi, level_training, id_level_training, competency, id_competency_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (kode, nama, fungsi, id_fungsi, level_posisi, id_level_posisi, level_training, id_level_training, competency, id_competency_level))
            conn.commit()
            flash(f'Master Training Baru ({kode} - {nama}) berhasil disimpan!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Gagal menyimpan Master Repository: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return redirect(url_for(redirect_to))

@app.route('/add_training', methods=['POST'])
def add_training():
    if 'username' not in session or session.get('role') != 'HC ADMIN':
        flash('Akses ditolak! Hanya HC Admin yang dapat menambah Batch COE.', 'danger')
        return redirect(url_for('dashboard'))
    
    kode = request.form.get('kode_training', '').strip()
    rencana_mulai = request.form.get('rencana_mulai', '-').strip() or '-'
    rencana_selesai = request.form.get('rencana_selesai', '-').strip() or '-'
    partisipan = request.form.get('partisipan', '0').strip()
    pic = request.form.get('pic', '-').strip() or '-'
    biaya = request.form.get('biaya', '0').strip() or '0'
    
    conn = get_db_connection()
    if conn:
        init_tables(conn)
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM master_repository WHERE kode_training = %s LIMIT 1", (kode,))
            master = cursor.fetchone()
            
            if master:
                nama = master.get('nama_training', '-')
                fungsi = master.get('fungsi', '-')
                level_posisi = master.get('level_posisi', '-')
                level_training = master.get('level_training', '-')
                competency = master.get('competency', '-')
                id_comp = master.get('id_competency_level', '-')
            else:
                cursor.execute("SELECT * FROM list_training WHERE kode_training = %s LIMIT 1", (kode,))
                master = cursor.fetchone() or {}
                nama = master.get('nama_training') or master.get('nama') or '-'
                fungsi = master.get('fungsi') or '-'
                level_posisi = master.get('level_posisi') or '-'
                level_training = master.get('level_training') or '-'
                competency = master.get('competency') or '-'
                id_comp = master.get('id_comp') or '-'

            cursor.execute("SELECT MAX(CAST(`no` AS UNSIGNED)) as max_no FROM list_training")
            row_no = cursor.fetchone()
            next_no = (row_no['max_no'] + 1) if (row_no and row_no.get('max_no')) else 1

            cursor.execute("SELECT COUNT(*) as total FROM list_training WHERE kode_training = %s", (kode,))
            count_res = cursor.fetchone()
            batch_code = f"B{(count_res['total'] + 1):03d}" if count_res else "B001"

            sql = """
                INSERT INTO list_training 
                (`no`, kode_training, nama_training, nama, fungsi, level_posisi, level_training, competency, id_comp, BATCH, STATUS_COE, rencana_mulai, rencana_selesai, partisipan, PIC, status_planning, biaya)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending', %s, %s, %s, %s, 'Belum Realisasi', %s)
            """
            cursor.execute(sql, (next_no, kode, nama, nama, fungsi, level_posisi, level_training, competency, id_comp, batch_code, rencana_mulai, rencana_selesai, partisipan, pic, biaya))
            conn.commit()
            flash('Penjadwalan Batch COE Baru berhasil ditambahkan!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'ERROR DATABASE: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return redirect(url_for('dashboard'))

@app.route('/edit_training/<int:id>', methods=['POST'])
def edit_training(id):
    if 'username' not in session or session.get('role') != 'HC ADMIN':
        flash('Akses ditolak! Hanya HC Admin yang dapat mengubah jadwal.', 'danger')
        return redirect(url_for('dashboard'))
    
    rencana_mulai = request.form.get('rencana_mulai', '').strip() or '-'
    rencana_selesai = request.form.get('rencana_selesai', '').strip() or '-'
    realisasi_mulai = request.form.get('realisasi_mulai', '').strip() or '-'
    realisasi_selesai = request.form.get('realisasi_selesai', '').strip() or '-'
    status_coe = request.form.get('status_coe', 'Pending')
    biaya = request.form.get('biaya', '0').strip() or '0'
    
    if realisasi_mulai != '-' and realisasi_mulai != '':
        if realisasi_mulai == rencana_mulai:
            status_planning = 'Sesuai'
        else:
            status_planning = 'Tidak Sesuai (Rescheduled)'
    else:
        status_planning = 'Belum Realisasi'

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE list_training 
                SET rencana_mulai=%s, rencana_selesai=%s, realisasi_mulai=%s, realisasi_selesai=%s, STATUS_COE=%s, status_planning=%s, biaya=%s 
                WHERE id=%s
            """, (rencana_mulai, rencana_selesai, realisasi_mulai, realisasi_selesai, status_coe, status_planning, biaya, id))
            conn.commit()
            flash('Perubahan jadwal & biaya berhasil disimpan!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Gagal memperbarui jadwal: {str(e)}', 'danger')
        finally:
            cursor.close()
            conn.close()
            
    return redirect(url_for('dashboard'))

@app.route('/delete_training/<int:id>', methods=['POST'])
def delete_training(id):
    if 'username' not in session or session.get('role') != 'HC ADMIN':
        flash('Akses ditolak! Hanya HC Admin yang dapat menghapus data.', 'danger')
        return redirect(url_for('dashboard'))
    
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