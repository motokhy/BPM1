"""
Script to fix a specific ERPProcess record in the database.
This ensures that the ID 101 exists in the erp_processes table.
"""
import os
import sys
from flask import Flask
from datetime import datetime
from backend.models.erp_process import ERPProcess, ERPProcessStep
from backend.models import db

# Create a minimal Flask app to use SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///instance/bpm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def fix_erp_process():
    """Ensure ERPProcess with ID 101 exists"""
    with app.app_context():
        # Check if process with ID 101 exists
        existing = ERPProcess.query.get(101)
        if existing:
            print(f"ERPProcess with ID 101 already exists: {existing.process_name}")
            print("Deleting and recreating to ensure integrity...")
            
            # Delete existing steps
            ERPProcessStep.query.filter_by(process_id=101).delete()
            # Delete existing process
            db.session.delete(existing)
            db.session.commit()
        
        # Create new process with ID 101
        process = ERPProcess(
            id=101,
            process_name='Invoice Processing',
            erp_system='Finance',
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(process)
        
        # Create steps for this process
        steps = [
            {'number': 1, 'description': 'Receive Invoice', 'approver_role': 'AP Clerk', 'approver_name': 'John Smith'},
            {'number': 2, 'description': 'Verify Invoice Details', 'approver_role': 'AP Specialist', 'approver_name': 'Sarah Johnson'},
            {'number': 3, 'description': 'Match with Purchase Order', 'approver_role': 'AP Specialist', 'approver_name': 'Sarah Johnson'},
            {'number': 4, 'description': 'Approval Workflow', 'approver_role': 'System', 'approver_name': 'ERP System'},
            {'number': 5, 'description': 'Process Payment', 'approver_role': 'Finance Manager', 'approver_name': 'Michael Chen'}
        ]
        
        for step_data in steps:
            step = ERPProcessStep(
                process_id=101,
                step_number=step_data['number'],
                step_description=step_data['description'],
                approver_role=step_data['approver_role'],
                approver_name=step_data['approver_name'],
                created_at=datetime.utcnow()
            )
            db.session.add(step)
        
        # Commit all changes
        db.session.commit()
        print("Successfully created/updated ERPProcess with ID 101")
        
        # Verify the process exists
        process = ERPProcess.query.get(101)
        if process:
            print(f"Verified: ERPProcess ID 101 - {process.process_name} exists in the database")
        else:
            print("ERROR: Failed to create ERPProcess with ID 101")

if __name__ == '__main__':
    fix_erp_process()
