"""
Script to initialize mock process data in the database.
This will create the sample processes that are currently
defined as mock data in the frontend.
"""
import os
import sys
from flask import Flask
from backend.models.erp_process import ERPProcess, ERPProcessStep
from backend.models import db

# Create a minimal Flask app to use SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL', 'sqlite:///instance/bpm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Mock process data - matching what's defined in the frontend
mock_processes = [
    # Finance processes (Category 1)
    {
        'id': 101,
        'name': 'Invoice Processing',
        'category': 'Finance',
        'steps': [
            {'number': 1, 'description': 'Receive Invoice', 'approver_role': 'AP Clerk', 'approver_name': 'John Smith'},
            {'number': 2, 'description': 'Verify Invoice Details', 'approver_role': 'AP Specialist', 'approver_name': 'Sarah Johnson'},
            {'number': 3, 'description': 'Match with Purchase Order', 'approver_role': 'AP Specialist', 'approver_name': 'Sarah Johnson'},
            {'number': 4, 'description': 'Approval Workflow', 'approver_role': 'System', 'approver_name': 'ERP System'},
            {'number': 5, 'description': 'Process Payment', 'approver_role': 'Finance Manager', 'approver_name': 'Michael Chen'}
        ]
    },
    {
        'id': 102,
        'name': 'Budget Approval',
        'category': 'Finance',
        'steps': [
            {'number': 1, 'description': 'Initiate Budget Request', 'approver_role': 'Department Head', 'approver_name': 'Department Manager'},
            {'number': 2, 'description': 'Complete Budget Form', 'approver_role': 'Department Head', 'approver_name': 'Department Manager'},
            {'number': 3, 'description': 'Department Manager Review', 'approver_role': 'Senior Manager', 'approver_name': 'Division Director'},
            {'number': 4, 'description': 'Finance Review', 'approver_role': 'Finance Analyst', 'approver_name': 'Emily Rodriguez'},
            {'number': 5, 'description': 'Finance Approval', 'approver_role': 'Finance Director', 'approver_name': 'Michael Chen'},
            {'number': 6, 'description': 'Executive Approval', 'approver_role': 'CFO', 'approver_name': 'Christopher Davis'}
        ]
    },
    {
        'id': 103,
        'name': 'Expense Reporting',
        'category': 'Finance',
        'steps': [
            {'number': 1, 'description': 'Submit Expense', 'approver_role': 'Employee', 'approver_name': 'Employee Name'},
            {'number': 2, 'description': 'Manager Review', 'approver_role': 'Manager', 'approver_name': 'Manager Name'},
            {'number': 3, 'description': 'Finance Review', 'approver_role': 'Finance Specialist', 'approver_name': 'Finance Team'},
            {'number': 4, 'description': 'Process Reimbursement', 'approver_role': 'Accounts Payable', 'approver_name': 'AP Team'}
        ]
    },
    # HR processes (Category 2) 
    {
        'id': 201,
        'name': 'Employee Onboarding',
        'category': 'HR',
        'steps': [
            {'number': 1, 'description': 'Job Requisition', 'approver_role': 'Hiring Manager', 'approver_name': 'Department Head'},
            {'number': 2, 'description': 'Screening Candidates', 'approver_role': 'HR Recruiter', 'approver_name': 'Jessica Miller'},
            {'number': 3, 'description': 'Interview Process', 'approver_role': 'HR/Manager', 'approver_name': 'Multiple Stakeholders'},
            {'number': 4, 'description': 'Select Candidate', 'approver_role': 'Hiring Manager', 'approver_name': 'Department Head'},
            {'number': 5, 'description': 'Make Offer', 'approver_role': 'HR', 'approver_name': 'Lisa Brown'},
            {'number': 6, 'description': 'Onboarding', 'approver_role': 'HR', 'approver_name': 'Maria Garcia'}
        ]
    },
    {
        'id': 202,
        'name': 'Performance Review',
        'category': 'HR',
        'steps': [
            {'number': 1, 'description': 'Schedule Review Period', 'approver_role': 'HR', 'approver_name': 'HR Director'},
            {'number': 2, 'description': 'Self Assessment', 'approver_role': 'Employee', 'approver_name': 'Employee Name'},
            {'number': 3, 'description': 'Manager Assessment', 'approver_role': 'Manager', 'approver_name': 'Manager Name'},
            {'number': 4, 'description': 'Review Meeting', 'approver_role': 'Manager', 'approver_name': 'Manager Name'},
            {'number': 5, 'description': 'Performance Rating', 'approver_role': 'Manager', 'approver_name': 'Manager Name'},
            {'number': 6, 'description': 'Document Results', 'approver_role': 'HR', 'approver_name': 'HR Specialist'}
        ]
    },
    {
        'id': 203,
        'name': 'Leave Request',
        'category': 'HR',
        'steps': [
            {'number': 1, 'description': 'Submit Request', 'approver_role': 'Employee', 'approver_name': 'Employee Name'},
            {'number': 2, 'description': 'Manager Review', 'approver_role': 'Manager', 'approver_name': 'Manager Name'},
            {'number': 3, 'description': 'HR Verification', 'approver_role': 'HR', 'approver_name': 'HR Specialist'},
            {'number': 4, 'description': 'Update System', 'approver_role': 'HR Admin', 'approver_name': 'HR Admin'},
            {'number': 5, 'description': 'Notify Teams', 'approver_role': 'Manager', 'approver_name': 'Manager Name'}
        ]
    },
    # Operations processes (Category 3)
    {
        'id': 301,
        'name': 'Lead Qualification',
        'category': 'Operations',
        'steps': [
            {'number': 1, 'description': 'Inbound Lead', 'approver_role': 'Marketing', 'approver_name': 'Marketing Team'},
            {'number': 2, 'description': 'Initial Assessment', 'approver_role': 'Sales Rep', 'approver_name': 'James Wilson'},
            {'number': 3, 'description': 'Qualification Check', 'approver_role': 'Sales Rep', 'approver_name': 'James Wilson'},
            {'number': 4, 'description': 'Schedule Demo', 'approver_role': 'Sales Rep', 'approver_name': 'Jessica Anderson'},
            {'number': 5, 'description': 'Add to Nurture', 'approver_role': 'Marketing', 'approver_name': 'Mark Williams'}
        ]
    },
    {
        'id': 302,
        'name': 'Quote Preparation',
        'category': 'Operations',
        'steps': [
            {'number': 1, 'description': 'Request Quote', 'approver_role': 'Customer', 'approver_name': 'Customer Name'},
            {'number': 2, 'description': 'Review Requirements', 'approver_role': 'Sales', 'approver_name': 'Robert Parker'},
            {'number': 3, 'description': 'Create Draft', 'approver_role': 'Sales Engineer', 'approver_name': 'Thomas White'},
            {'number': 4, 'description': 'Internal Review', 'approver_role': 'Sales Manager', 'approver_name': 'Jennifer Lee'},
            {'number': 5, 'description': 'Executive Approval', 'approver_role': 'Executive', 'approver_name': 'Christopher Davis'},
            {'number': 6, 'description': 'Execute Contract', 'approver_role': 'Sales Director', 'approver_name': 'Daniel Murphy'}
        ]
    },
    # IT processes (Category 4)
    {
        'id': 401,
        'name': 'Incident Management',
        'category': 'IT',
        'steps': [
            {'number': 1, 'description': 'Incident Reported', 'approver_role': 'User', 'approver_name': 'End User'},
            {'number': 2, 'description': 'Ticket Created', 'approver_role': 'Helpdesk', 'approver_name': 'Support Tier 1'},
            {'number': 3, 'description': 'Initial Diagnosis', 'approver_role': 'Support', 'approver_name': 'Support Tier 1'},
            {'number': 4, 'description': 'Escalation if Needed', 'approver_role': 'Support', 'approver_name': 'Support Tier 2'},
            {'number': 5, 'description': 'Resolution', 'approver_role': 'Support', 'approver_name': 'Support Engineer'},
            {'number': 6, 'description': 'Verification', 'approver_role': 'User', 'approver_name': 'End User'},
            {'number': 7, 'description': 'Ticket Closure', 'approver_role': 'Helpdesk', 'approver_name': 'Support Tier 1'}
        ]
    },
    {
        'id': 402,
        'name': 'System Deployment',
        'category': 'IT',
        'steps': [
            {'number': 1, 'description': 'Requirement Analysis', 'approver_role': 'System Analyst', 'approver_name': 'IT Analyst'},
            {'number': 2, 'description': 'System Design', 'approver_role': 'Architect', 'approver_name': 'IT Architect'},
            {'number': 3, 'description': 'Development', 'approver_role': 'Developer', 'approver_name': 'Development Team'},
            {'number': 4, 'description': 'Testing', 'approver_role': 'QA', 'approver_name': 'QA Team'},
            {'number': 5, 'description': 'UAT', 'approver_role': 'Business', 'approver_name': 'Business Users'},
            {'number': 6, 'description': 'Deployment', 'approver_role': 'DevOps', 'approver_name': 'Operations Team'},
            {'number': 7, 'description': 'Post-Deployment Review', 'approver_role': 'Project Manager', 'approver_name': 'PM Team'}
        ]
    },
    {
        'id': 403,
        'name': 'Data Backup',
        'category': 'IT',
        'steps': [
            {'number': 1, 'description': 'Identify Data', 'approver_role': 'Data Owner', 'approver_name': 'Department Head'},
            {'number': 2, 'description': 'Define Schedule', 'approver_role': 'IT Admin', 'approver_name': 'IT Operations'},
            {'number': 3, 'description': 'Configure Backup', 'approver_role': 'IT Admin', 'approver_name': 'IT Operations'},
            {'number': 4, 'description': 'Execute Backup', 'approver_role': 'System', 'approver_name': 'Automated System'},
            {'number': 5, 'description': 'Verify Backup', 'approver_role': 'IT Admin', 'approver_name': 'IT Operations'},
            {'number': 6, 'description': 'Store Securely', 'approver_role': 'IT Security', 'approver_name': 'Security Team'}
        ]
    }
]

def setup_mock_data():
    """Insert the mock process data into the database"""
    with app.app_context():
        print("Setting up mock process data...")
        
        # Create processes
        for process_data in mock_processes:
            # Check if process with this ID already exists
            existing = ERPProcess.query.get(process_data['id'])
            if existing:
                print(f"Process {process_data['id']} - {process_data['name']} already exists, skipping...")
                continue
                
            # Create new process
            process = ERPProcess(
                id=process_data['id'],
                process_name=process_data['name'],
                erp_system=process_data['category'],
                created_at=db.func.now(),
                updated_at=db.func.now()
            )
            db.session.add(process)
            
            # Create steps for this process
            for step_data in process_data['steps']:
                step = ERPProcessStep(
                    process_id=process_data['id'],
                    step_number=step_data['number'],
                    step_description=step_data['description'],
                    approver_role=step_data['approver_role'],
                    approver_name=step_data['approver_name'],
                    created_at=db.func.now()
                )
                db.session.add(step)
                
            print(f"Added process: {process_data['name']} with {len(process_data['steps'])} steps")
            
        # Commit all changes
        db.session.commit()
        print("Mock data setup complete.")

if __name__ == '__main__':
    setup_mock_data()
