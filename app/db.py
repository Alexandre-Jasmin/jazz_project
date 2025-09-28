import os
import pymysql

from config import DevelopmentConfig

def get_connection():
    return pymysql.connect(
        host=DevelopmentConfig.LEAGUE_DB_HOST,
        user=DevelopmentConfig.LEAGUE_DB_USER,
        password=DevelopmentConfig.LEAGUE_DB_PASSWORD,
        database=DevelopmentConfig.LEAGUE_DB_NAME,
        port=DevelopmentConfig.LEAGUE_DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

def load_sql(filename: str) -> str:
    file_path = os.path.join(DevelopmentConfig.BASE_SQL_DIR, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

class DBConnection:
    def __enter__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.cursor.close()
        self.conn.close()

    def execute_sql(self, filename: str, params: tuple = ()):
        sql = load_sql(filename)
        self.cursor.execute(sql, params)
        return self.cursor

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()
