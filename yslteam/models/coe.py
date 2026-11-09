from .database import get_db


def add_coe_schedule(kode, batch, status, ren_m, ren_s, partisipan, pic):
    """Tambah jadwal batch COE baru."""
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO coe_schedule
        (kode_training, batch, status_coe, tgl_rencana_mulai, tgl_rencana_selesai, jumlah_partisipan, pic)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (kode, batch, status, ren_m, ren_s, partisipan, pic))
    db.commit()
    cur.close()
    db.close()


def update_coe_schedule(id_coe, rea_m, rea_s, status_coe):
    """Update realisasi dan status jadwal COE."""
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE coe_schedule
        SET tgl_realisasi_mulai = %s, tgl_realisasi_selesai = %s, status_coe = %s
        WHERE id_coe = %s
    """, (rea_m if rea_m else None, rea_s if rea_s else None, status_coe, id_coe))
    db.commit()
    cur.close()
    db.close()


def delete_coe_schedule(id_coe):
    """Hapus jadwal COE berdasarkan id_coe."""
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM coe_schedule WHERE id_coe = %s", (id_coe,))
    db.commit()
    cur.close()
    db.close()
