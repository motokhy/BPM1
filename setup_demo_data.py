import os
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

# Import models and Base
from models.erp_process import ERPProcess, ERPProcessStep, db
from models.tobe_process import ToBeProcess, ToBeProcessStep, GapAnalysis, GapFinding

# Create database connection
db_path = os.path.join(backend_dir, 'bpm.db')
engine = create_engine(f'sqlite:///{db_path}')

# Create all tables
print("Creating tables...")
db.Model.metadata.create_all(bind=engine)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

def create_demo_data():
    print("Creating demo data...")
    
    # Purchase Order Approval Process
    po_process = ERPProcess(
        process_name="Purchase Order Approval",
        erp_system="SAP",
        created_at=datetime.utcnow()
    )
    session.add(po_process)
    session.flush()

    po_steps = [
        (1, "PO Creation by Requester", "Requester", "John Smith"),
        (2, "Department Manager Review", "Manager", "Sarah Johnson"),
        (3, "Finance Team Validation", "Finance", "Mike Wilson"),
        (4, "Final Approval", "Procurement", "Lisa Chen"),
        (5, "PO Generation", "System", "Automated")
    ]

    for step_num, desc, role, name in po_steps:
        step = ERPProcessStep(
            process_id=po_process.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # Employee Onboarding Process
    onboard_process = ERPProcess(
        process_name="Employee Onboarding",
        erp_system="Workday",
        created_at=datetime.utcnow()
    )
    session.add(onboard_process)
    session.flush()

    onboard_steps = [
        (1, "Offer Letter Acceptance", "HR", "Emma Davis"),
        (2, "Background Check", "HR", "Emma Davis"),
        (3, "IT Equipment Setup", "IT", "Tech Support"),
        (4, "System Access Provisioning", "IT Security", "James Wilson"),
        (5, "HR Documentation", "HR", "Emma Davis"),
        (6, "Department Orientation", "Department Manager", "Team Lead")
    ]

    for step_num, desc, role, name in onboard_steps:
        step = ERPProcessStep(
            process_id=onboard_process.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # Invoice Processing
    invoice_process = ERPProcess(
        process_name="Invoice Processing",
        erp_system="Oracle",
        created_at=datetime.utcnow()
    )
    session.add(invoice_process)
    session.flush()

    invoice_steps = [
        (1, "Invoice Receipt", "AP Clerk", "Robert Brown"),
        (2, "Invoice Data Entry", "AP Clerk", "Robert Brown"),
        (3, "PO Matching", "System", "Automated"),
        (4, "Discrepancy Resolution", "AP Manager", "Patricia White"),
        (5, "Payment Authorization", "Finance Manager", "David Lee"),
        (6, "Payment Processing", "System", "Automated")
    ]

    for step_num, desc, role, name in invoice_steps:
        step = ERPProcessStep(
            process_id=invoice_process.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # Create TO-BE Processes for demo
    # 1. TO-BE Process for Invoice Processing using American Standard
    tobe_invoice_american = ToBeProcess(
        process_name="TO-BE: Invoice Processing (American Standard)",
        related_asis_id=invoice_process.id,
        standard_type="american",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(tobe_invoice_american)
    session.flush()

    tobe_invoice_american_steps = [
        (1, "Electronic Invoice Receipt", "System", "Automated", True),
        (2, "Automated Data Extraction", "System", "Automated", True),
        (3, "PO Matching and Validation", "System", "Automated", True),
        (4, "Exception Handling", "AP Specialist", "Robert Brown", False),
        (5, "Approval Workflow", "System", "Automated", True),
        (6, "Payment Scheduling", "Finance Manager", "David Lee", False),
        (7, "Automated Payment Processing", "System", "Automated", True)
    ]

    for step_num, desc, role, name, is_auto in tobe_invoice_american_steps:
        step = ToBeProcessStep(
            process_id=tobe_invoice_american.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            is_automated=is_auto,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # 2. TO-BE Process for Employee Onboarding using Japanese Standard
    tobe_onboard_japanese = ToBeProcess(
        process_name="TO-BE: Employee Onboarding (Japanese Standard)",
        related_asis_id=onboard_process.id,
        standard_type="japanese",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(tobe_onboard_japanese)
    session.flush()

    tobe_onboard_japanese_steps = [
        (1, "Digital Offer Acceptance and Documentation", "HR", "Emma Davis", True),
        (2, "Automated Background Check Integration", "System", "Automated", True),
        (3, "Self-Service Portal Access", "New Employee", "Various", False),
        (4, "Just-in-Time Equipment Preparation", "IT", "Tech Support", False),
        (5, "Automated System Access Provisioning", "System", "Automated", True),
        (6, "Digital Training Assignment", "HR", "Emma Davis", True),
        (7, "Mentorship Assignment", "Department Manager", "Team Lead", False),
        (8, "Continuous Feedback Loop", "HR", "Emma Davis", False)
    ]

    for step_num, desc, role, name, is_auto in tobe_onboard_japanese_steps:
        step = ToBeProcessStep(
            process_id=tobe_onboard_japanese.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            is_automated=is_auto,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # 3. TO-BE Process for Purchase Order using ISO Standard
    tobe_po_iso = ToBeProcess(
        process_name="TO-BE: Purchase Order Approval (ISO Standard)",
        related_asis_id=po_process.id,
        standard_type="iso",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(tobe_po_iso)
    session.flush()

    tobe_po_iso_steps = [
        (1, "Standardized Requisition Form Submission", "Requester", "John Smith", False),
        (2, "Automated Budget Validation", "System", "Automated", True),
        (3, "Risk Assessment", "Risk Manager", "Alex Torres", False),
        (4, "Tiered Approval Based on Value", "System", "Automated", True),
        (5, "Compliance Check", "Compliance Officer", "Maria Garcia", False),
        (6, "Vendor Selection Validation", "Procurement", "Lisa Chen", False),
        (7, "Automated PO Generation", "System", "Automated", True),
        (8, "Quality Management Record", "Quality Officer", "Sam Lee", False)
    ]

    for step_num, desc, role, name, is_auto in tobe_po_iso_steps:
        step = ToBeProcessStep(
            process_id=tobe_po_iso.id,
            step_number=step_num,
            step_description=desc,
            approver_role=role,
            approver_name=name,
            is_automated=is_auto,
            created_at=datetime.utcnow()
        )
        session.add(step)

    # Create Gap Analysis for demonstration
    # 1. Gap Analysis for Invoice Processing
    invoice_gap = GapAnalysis(
        asis_process_id=invoice_process.id,
        tobe_process_id=tobe_invoice_american.id,
        created_at=datetime.utcnow(),
        summary="The current invoice processing workflow has several manual steps that could be automated. The TO-BE process introduces automation at key points to reduce processing time and errors."
    )
    session.add(invoice_gap)
    session.flush()

    invoice_findings = [
        ("Automation", "Manual data entry is time-consuming and error-prone", "Implement OCR and AI-based data extraction to automate invoice data capture", "High", "Medium"),
        ("Inefficient", "PO matching is automated but discrepancy resolution is manual and time-consuming", "Implement intelligent exception handling with suggested resolutions", "Medium", "Low"),
        ("Compliance", "Lack of systematic audit trail for approvals", "Add digital signature and timestamping for all approvals", "High", "Low"),
        ("Resource", "AP clerk time is spent on low-value data entry tasks", "Redirect AP personnel to exception handling and vendor relationship management", "Medium", "Medium")
    ]

    for f_type, desc, rec, impact, effort in invoice_findings:
        finding = GapFinding(
            analysis_id=invoice_gap.id,
            finding_type=f_type,
            description=desc,
            recommendation=rec,
            impact=impact,
            effort=effort,
            created_at=datetime.utcnow()
        )
        session.add(finding)

    # 2. Gap Analysis for Employee Onboarding
    onboard_gap = GapAnalysis(
        asis_process_id=onboard_process.id,
        tobe_process_id=tobe_onboard_japanese.id,
        created_at=datetime.utcnow(),
        summary="The current onboarding process has fragmented steps across departments with limited automation. The TO-BE process introduces self-service elements and continuous improvement concepts from Kaizen methodology."
    )
    session.add(onboard_gap)
    session.flush()

    onboard_findings = [
        ("Missing", "No formal feedback mechanism during onboarding", "Implement continuous feedback loop with regular check-ins", "Medium", "Low"),
        ("Inefficient", "Separate steps for documentation and system access", "Create unified digital onboarding portal", "High", "Medium"),
        ("Automation", "Manual equipment setup process", "Implement automated provisioning system tied to HR approval", "Medium", "High"),
        ("Resource", "HR staff handling repetitive documentation tasks", "Move to self-service portal with HR oversight only for exceptions", "High", "Medium")
    ]

    for f_type, desc, rec, impact, effort in onboard_findings:
        finding = GapFinding(
            analysis_id=onboard_gap.id,
            finding_type=f_type,
            description=desc,
            recommendation=rec,
            impact=impact,
            effort=effort,
            created_at=datetime.utcnow()
        )
        session.add(finding)

    # Commit changes
    session.commit()
    print("Demo data created successfully!")

if __name__ == "__main__":
    # Clear existing data
    session.query(GapFinding).delete()
    session.query(GapAnalysis).delete()
    session.query(ToBeProcessStep).delete()
    session.query(ToBeProcess).delete()
    session.query(ERPProcessStep).delete()
    session.query(ERPProcess).delete()
    session.commit()
    
    # Create new demo data
    create_demo_data()
