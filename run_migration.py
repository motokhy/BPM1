"""
Run the migration to update the tobe_processes table
"""
from backend import create_app, db
from backend.migrations.update_tobe_process import upgrade

def run_migration():
    app = create_app()
    with app.app_context():
        print("Running migration to update tobe_processes table...")
        upgrade()
        print("Migration completed successfully!")

if __name__ == "__main__":
    run_migration()
