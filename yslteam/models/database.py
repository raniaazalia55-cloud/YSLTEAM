import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from flask import current_app


def get_db():
    """Membuat dan mengembalikan koneksi database MySQL."""
    return MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        port=current_app.config.get('MYSQL_PORT', 3306),
        user=current_app.config['MYSQL_USER'],
        password=current_app.config['MYSQL_PASSWORD'],
        database=current_app.config['MYSQL_DB'],
        cursorclass=MySQLdb.cursors.DictCursor
    )
