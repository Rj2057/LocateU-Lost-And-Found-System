# backend/display.py
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import DatabaseConfig
from mysql.connector import Error

def display_table_structure():
    """Display all tables with their structure and constraints"""
    connection = DatabaseConfig.get_connection()
    if not connection:
        print("❌ Failed to connect to database")
        return
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get all tables in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("=" * 80)
        print("DATABASE: LostAndFoundDB - TABLE STRUCTURE AND CONSTRAINTS")
        print("=" * 80)
        
        for table in tables:
            table_name = table[f"Tables_in_{DatabaseConfig.DB_CONFIG['database'].lower()}"]
            print(f"\n📊 TABLE: {table_name}")
            print("-" * 60)
            
            # Display table columns and constraints
            cursor.execute(f"DESCRIBE {table_name}")
            columns = cursor.fetchall()
            
            print(f"{'Column':<20} {'Type':<20} {'Null':<8} {'Key':<10} {'Default':<15} {'Extra':<10}")
            print("-" * 90)
            for column in columns:
                default_value = str(column['Default']) if column['Default'] is not None else 'NULL'
                print(f"{column['Field']:<20} {column['Type']:<20} {column['Null']:<8} {column['Key']:<10} {default_value:<15} {column['Extra']:<10}")
            
            # Display foreign key constraints
            print(f"\n🔗 FOREIGN KEY CONSTRAINTS for {table_name}:")
            cursor.execute(f"""
                SELECT 
                    CONSTRAINT_NAME,
                    COLUMN_NAME,
                    REFERENCED_TABLE_NAME,
                    REFERENCED_COLUMN_NAME
                FROM information_schema.KEY_COLUMN_USAGE
                WHERE TABLE_SCHEMA = '{DatabaseConfig.DB_CONFIG['database']}' 
                AND TABLE_NAME = '{table_name}'
                AND REFERENCED_TABLE_NAME IS NOT NULL
            """)
            foreign_keys = cursor.fetchall()
            
            if foreign_keys:
                for fk in foreign_keys:
                    print(f"   {fk['COLUMN_NAME']} → {fk['REFERENCED_TABLE_NAME']}({fk['REFERENCED_COLUMN_NAME']})")
            else:
                print("   No foreign keys")
            
            print("\n" + "=" * 80)
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

def display_sample_data():
    """Display sample data from each table"""
    connection = DatabaseConfig.get_connection()
    if not connection:
        return
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        print("\n" + "=" * 80)
        print("SAMPLE DATA FROM TABLES (First 2 rows)")
        print("=" * 80)
        
        for table in tables:
            table_name = table[f"Tables_in_{DatabaseConfig.DB_CONFIG['database'].lower()}"]
            print(f"\n📋 DATA FROM: {table_name}")
            print("-" * 60)
            
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
            rows = cursor.fetchall()
            
            if rows:
                # Print column headers
                columns = rows[0].keys()
                header = " | ".join(str(col) for col in columns)
                print(header)
                print("-" * len(header))
                
                # Print data rows
                for row in rows:
                    values = [str(row[col])[:30] + "..." if len(str(row[col])) > 30 else str(row[col]) for col in columns]
                    print(" | ".join(values))
            else:
                print("No data found")
            
            # Show total count
            cursor.execute(f"SELECT COUNT(*) as total FROM {table_name}")
            total = cursor.fetchone()['total']
            print(f"Total rows: {total}")
    
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    display_table_structure()
    display_sample_data()