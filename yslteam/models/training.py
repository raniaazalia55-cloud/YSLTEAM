from .database import get_db


def get_all_training_with_schedule():
    """Ambil semua data training yang sudah memiliki jadwal COE (INNER JOIN)."""
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT
            r.kode_training, r.fungsi, r.id_fungsi, r.level_posisi, r.id_level_posisi,
            r.level_training, r.id_level_training, r.group_posisi, r.id_group_posisi,
            r.nama_training, r.egi, r.competency, r.id_competency_level,
            c.id_coe, c.batch, c.status_coe, c.tgl_rencana_mulai, c.tgl_rencana_selesai,
            c.tgl_realisasi_mulai, c.tgl_realisasi_selesai, c.jumlah_partisipan,
            c.durasi_jam, c.penyelenggara, c.lokasi, c.pic
        FROM training_repository r
        INNER JOIN coe_schedule c ON r.kode_training = c.kode_training
        ORDER BY r.kode_training ASC, c.batch ASC
    """)
    rows = cur.fetchall()
    cur.close()
    db.close()
    return rows


def get_all_repository():
    """Ambil semua master training dari repository."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM training_repository ORDER BY kode_training ASC")
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


def get_repository_list():
    """Ambil daftar ringkas training (kode & nama) untuk dropdown."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT kode_training, nama_training FROM training_repository ORDER BY kode_training ASC")
    data = cur.fetchall()
    cur.close()
    db.close()
    return data


def add_repository(kode, nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos,
                   lvl_train, id_lvl_train, comp, id_comp):
    """Tambah master training baru. Raise ValueError jika kode sudah ada."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT kode_training FROM training_repository WHERE kode_training = %s", (kode,))
    if cur.fetchone():
        cur.close()
        db.close()
        raise ValueError(f'Kode Training {kode} sudah terdaftar di Repository!')
    cur.execute("""
        INSERT INTO training_repository
        (kode_training, fungsi, id_fungsi, level_posisi, id_level_posisi,
         level_training, id_level_training, nama_training, competency, id_competency_level)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (kode, fungsi, id_fungsi, lvl_pos, id_lvl_pos, lvl_train, id_lvl_train, nama, comp, id_comp))
    db.commit()
    cur.close()
    db.close()


def update_repository(kode, nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos,
                      lvl_train, id_lvl_train, comp, id_comp):
    """Update data master training berdasarkan kode_training."""
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE training_repository
        SET nama_training=%s, fungsi=%s, id_fungsi=%s, level_posisi=%s, id_level_posisi=%s,
            level_training=%s, id_level_training=%s, competency=%s, id_competency_level=%s
        WHERE kode_training=%s
    """, (nama, fungsi, id_fungsi, lvl_pos, id_lvl_pos, lvl_train, id_lvl_train, comp, id_comp, kode))
    db.commit()
    cur.close()
    db.close()


def delete_repository(kode_training):
    """Hapus master training (batch COE terkait ikut terhapus via CASCADE)."""
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM training_repository WHERE kode_training = %s", (kode_training,))
    db.commit()
    cur.close()
    db.close()
