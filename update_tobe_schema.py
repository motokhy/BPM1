"""
Update the tobe_processes table schema to make related_asis_id nullable.
This script will alter the existing table structure in SQLite.
"""
import os
import sys
from flask import Flask
import sqlite3

# Create a minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///instance/bpm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def update_schema():
    """Update the tobe_processes table schema"""
    # Get the database path from the Flask config
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    print(f"Using database at: {db_path}")
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Step 1: Get the current table create statement
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tobe_processes'")
        create_stmt = cursor.fetchone()[0]
        print(f"Current schema: {create_stmt}")
        
        # Step 2: Create a new temporary table with the updated schema
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tobe_processes_new (
            id INTEGER NOT NULL, 
            process_name VARCHAR(255) NOT NULL, 
            related_asis_id INTEGER, 
            standard_type VARCHAR(100) NOT NULL, 
            created_at DATETIME, 
            updated_at DATETIME, 
            PRIMARY KEY (id), 
            FOREIGN KEY(related_asis_id) REFERENCES erp_processes (id) ON DELETE SET NULL
        )
        """)
        
        # Step 3: Copy data from the old table to the new one
        cursor.execute("INSERT OR IGNORE INTO tobe_processes_new SELECT id, process_name, related_asis_id, standard_type, created_at, updated_at FROM tobe_processes")
        
        # Step 4: Drop the old table
        cursor.execute("DROP TABLE tobe_processes")
        
        # Step 5: Rename the new table to the original name
        cursor.execute("ALTER TABLE tobe_processes_new RENAME TO tobe_processes")
        
        # Commit the changes
        conn.commit()
        print("Successfully updated tobe_processes table schema")
        
    except Exception as e:
        print(f"Error updating schema: {str(e)}")
        conn.rollback()
    finally:
        # Verify the new schema
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tobe_processes'")
        new_create_stmt = cursor.fetchone()
        if new_create_stmt:
            print(f"New schema: {new_create_stmt[0]}")
        else:
            print("WARNING: Could not retrieve new schema")
            
        conn.close()

if __name__ == '__main__':
    update_schema()
