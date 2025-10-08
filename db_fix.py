"""
Direct database fix script to update the tobe_processes table structure
"""
import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

def fix_database():
    load_dotenv()
    
    # Get the database path from environment or use default
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///instance/bpm_system.db')
    
    print(f"Connecting to database: {db_url}")
    
    try:
        # Extract the SQLite database path from the URL
        if db_url.startswith('sqlite:///'):
            db_path = db_url.replace('sqlite:///', '')
            # Handle relative paths
            if not os.path.isabs(db_path):
                # If it's a relative path, make it relative to the current directory
                db_path = os.path.join(os.getcwd(), db_path)
        else:
            # Try to extract from full path
            db_path = db_url
        
        print(f"Using database at: {db_path}")
        
        # Check if the database file exists
        if not os.path.exists(db_path):
            print(f"Database file not found at {db_path}")
            return False
            
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = conn.cursor()
        
        # Check if tobe_processes table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tobe_processes'")
        table_exists = cursor.fetchone() is not None
        
        if not table_exists:
            print("tobe_processes table does not exist, no fix needed")
            conn.close()
            return True
        
        # Get the current table structure
        cursor.execute("PRAGMA table_info(tobe_processes)")
        columns = cursor.fetchall()
        column_names = [column['name'] for column in columns]
        
        # Check if process_type column exists
        if 'process_type' not in column_names:
            print("Adding process_type column...")
            cursor.execute("ALTER TABLE tobe_processes ADD COLUMN process_type TEXT NOT NULL DEFAULT 'asis'")
        
        # In SQLite, we need to recreate the table to remove foreign key constraints
        print("Creating temporary table without foreign key constraint...")
        cursor.execute("""
        CREATE TABLE tobe_processes_new (
            id INTEGER PRIMARY KEY,
            process_name TEXT NOT NULL,
            related_asis_id INTEGER,
            process_type TEXT NOT NULL DEFAULT 'asis',
            standard_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Copy data to the new table
        print("Copying data to new table...")
        cursor.execute("""
        INSERT INTO tobe_processes_new 
        SELECT id, process_name, related_asis_id, 
               CASE WHEN process_type IS NULL THEN 'asis' ELSE process_type END,
               standard_type, created_at, updated_at 
        FROM tobe_processes
        """)
        
        # Drop the old table
        print("Dropping old table...")
        cursor.execute("DROP TABLE tobe_processes")
        
        # Rename the new table
        print("Renaming new table...")
        cursor.execute("ALTER TABLE tobe_processes_new RENAME TO tobe_processes")
        
        # Commit the changes
        conn.commit()
        print("Database structure updated successfully!")
        
        # Close the connection
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error updating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    fix_database()
