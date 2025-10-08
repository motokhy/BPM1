import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os
import sys

def setup_database():
    """Set up the PostgreSQL database for the BPM system"""
    load_dotenv()
    
    # Get database configuration from environment
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL not found in environment variables")
        sys.exit(1)

    # Parse database URL
    # Format: postgresql://postgres:password@localhost:5432/bpm_db
    try:
        # Connect to PostgreSQL server to create database if it doesn't exist
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="SOLOm_4/10/1991",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        
        # Create database if it doesn't exist
        cur.execute("SELECT 1 FROM pg_database WHERE datname='bpm_db'")
        if cur.fetchone() is None:
            cur.execute("CREATE DATABASE bpm_db")
            print("Database 'bpm_db' created successfully")
        else:
            print("Database 'bpm_db' already exists")
            
        cur.close()
        conn.close()
        
        print("Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
