# backend/config.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).parent.parent
env_path = root_dir / '.env'
load_dotenv(env_path)

class DatabaseConfig:
    DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'LostAndFoundDB'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
        'collation': 'utf8mb4_unicode_ci',
        'autocommit': True,
        'raise_on_warnings': True
    }
    
    @staticmethod
    def get_connection():
        """Establish and return database connection"""
        try:
            connection = mysql.connector.connect(**DatabaseConfig.DB_CONFIG)
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"✅ Successfully connected to MySQL Server version {db_info}")
                print(f"📊 Database: {DatabaseConfig.DB_CONFIG['database']}")
                return connection
        except Error as e:
            print(f"❌ Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def test_connection():
        """Test the database connection and display basic info"""
        try:
            connection = DatabaseConfig.get_connection()
            if connection:
                cursor = connection.cursor()

                cursor.execute("SELECT DATABASE()")
                db_name = cursor.fetchone()
                print(f"🎯 Current database: {db_name[0]}")

                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                print("📋 Tables in database:")
                for table in tables:
                    print(f"   - {table[0]}")

                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = cursor.fetchone()[0]
                    print(f"   - {table_name}: {count} rows")
                
                cursor.close()
                connection.close()
                print("🔌 Connection closed")
                return True
        except Error as e:
            print(f"❌ Connection test failed: {e}")
            return False

    @staticmethod
    def get_config():
        """Return database configuration (without password) for debugging"""
        config = DatabaseConfig.DB_CONFIG.copy()
        config['password'] = '***HIDDEN***'
        return config

if __name__ == "__main__":
    print("🔧 Testing database connection...")
    print(f"📝 Configuration: {DatabaseConfig.get_config()}")
    print("-" * 50)
    DatabaseConfig.test_connection()