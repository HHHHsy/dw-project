import sys
import os
sys.path.insert(0, os.getcwd())
import pymysql

try:
    # First, connect to MySQL server to create the database if it doesn't exist
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='hrxcy31.',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS python_edu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database created or already exists.")

    # Now connect to the created database to create tables
    conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='hrxcy31.',
        database='python_edu',
        charset='utf8mb4'
    )
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Table 'users' created successfully.")
except Exception as e:
    print(f"Error initializing database: {e}")
