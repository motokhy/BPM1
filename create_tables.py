from app import create_app
from backend.models import db

def create_tables():
    """Create database tables directly using SQLAlchemy"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        try:
            db.create_all()
            print("Successfully created all database tables!")
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

if __name__ == "__main__":
    create_tables()
