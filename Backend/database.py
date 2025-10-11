
# ====================================
# FILE: backend/database.py
# ====================================
import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():

    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset=Config.DB_CHARSET
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False, fetchone=False):

    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchone() if fetchone else cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid if cursor.lastrowid else True
    except Error as e:
        print(f"Database error: {e}")
        connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def call_procedure(proc_name, params=()):

    connection = get_db_connection()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        cursor.callproc(proc_name, params)
        connection.commit()
        return True
    except Error as e:
        print(f"Procedure error: {e}")
        connection.rollback()
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def call_function(func_query):

    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor()
        cursor.execute(func_query)
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


print("\nBackend configuration files created!")
print("Now creating main Flask application...")

print("\n" + "=" * 50)
print("NEXT: Creating app.py (Flask Application)")
print("=" * 50)