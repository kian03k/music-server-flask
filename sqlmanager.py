import pymysql
from pymysql import MySQLError

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "MyStrongPassword123!",
    "database": "music_platform",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_conn():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        return conn, cursor
    except MySQLError as e:
        print("数据库连接失败:", e)
        return None, None

def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def get_all_users():
    conn, cursor = get_conn()
    if not conn:
        return []
    try:
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    finally:
        close_conn(conn, cursor)

def add_user(user_data):
    conn, cursor = get_conn()
    if not conn:
        return False
    try:
        keys = ", ".join(user_data.keys())
        placeholders = ", ".join(["%s"] * len(user_data))
        sql = f"INSERT INTO users ({keys}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(user_data.values()))
        conn.commit()
        return True
    except MySQLError as e:
        print("添加失败:", e)
        conn.rollback()
        return False
    finally:
        close_conn(conn, cursor)

def delete_user(user_id):
    conn, cursor = get_conn()
    if not conn:
        return False
    try:
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        close_conn(conn, cursor)

def update_user(user_info):
    conn, cursor = get_conn()
    if not conn:
        return False
    try:
        sql = """
            UPDATE users SET
                name   = %s,
                addr   = %s,
                age    = %s,
                birth  = %s,
                sex    = %s
            WHERE id = %s
        """
        params = (
            user_info["name"],
            user_info["addr"],
            user_info["age"],
            user_info["birth"],
            user_info["sex"],
            user_info["id"]
        )
        cursor.execute(sql, params)
        conn.commit()
        return True
    finally:
        close_conn(conn, cursor)

def login_user(name, password):
    conn, cursor = get_conn()
    if not conn:
        return None
    try:
        cursor.execute("SELECT * FROM users WHERE name = %s AND password = %s", (name, password))
        return cursor.fetchone()
    finally:
        close_conn(conn, cursor)

def clear_users():
    conn, cursor = get_conn()
    if not conn:
        return False
    try:
        cursor.execute("TRUNCATE TABLE users")
        conn.commit()
        return True
    finally:
        close_conn(conn, cursor)