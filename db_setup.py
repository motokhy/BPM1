from app import create_app
from backend.models import db, ERPProcess, ERPProcessStep
from datetime import datetime

def setup_database():
    """Initialize the database with tables and sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

        # Add sample data
        sample_po_process = ERPProcess(
            process_name="Purchase Order Approval",
            erp_system="SAP",
            created_at=datetime.utcnow()
        )
        db.session.add(sample_po_process)
        db.session.flush()  # Get the ID before adding steps

        po_steps = [
            (1, "PO Creation by Requester", "Requester", "John Smith"),
            (2, "Department Manager Review", "Manager", "Sarah Johnson"),
            (3, "Finance Team Validation", "Finance", "Mike Wilson"),
            (4, "Final Approval", "Procurement", "Lisa Chen"),
            (5, "PO Generation", "System", "Automated")
        ]

        for step_num, desc, role, name in po_steps:
            step = ERPProcessStep(
                process_id=sample_po_process.id,
                step_number=step_num,
                step_description=desc,
                approver_role=role,
                approver_name=name,
                created_at=datetime.utcnow()
            )
            db.session.add(step)

        try:
            db.session.commit()
            print("Sample data added successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding sample data: {str(e)}")
            raise

if __name__ == "__main__":
    setup_database()
