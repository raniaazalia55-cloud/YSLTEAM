import os
import mysql.connector

def run_import():
    try:
        # Koneksi ke MySQL Railway
        conn = mysql.connector.connect(
            host='metro.proxy.rlwy.net',
            port=25400,
            user='root',
            password='zcpfSAJevVOUTOlxEVSXPFnUJyoQgmkW',
            database='railway'
        )
        cursor = conn.cursor()
        
        # Buka dan baca file yslteam.sql
        with open('yslteam.sql', 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # Jalankan setiap query SQL
        commands = sql_script.split(';')
        for command in commands:
            cmd = command.strip()
            if cmd:
                cursor.execute(cmd)
        
        conn.commit()
        print("✅ DATABASE BERHASIL DI-IMPORT 100%!")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Gagal import database: {e}")

if __name__ == '__main__':
    run_import()