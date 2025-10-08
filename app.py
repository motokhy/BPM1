from flask import Flask, render_template, send_from_directory, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import json
import logging
from datetime import datetime
from fpdf import FPDF

# Try importing SocketIO, but make it optional
try:
    from flask_socketio import SocketIO
    socketio_available = True
except ImportError:
    socketio_available = False
    print("WARNING: flask_socketio not available. WebSocket functionality will be disabled.")

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    # Use relative paths for static and template folders
    app = Flask(__name__,
            static_folder='/home/ec2-user/AI-powered-BPM/react-frontend/dist',
            template_folder='/home/ec2-user/AI-powered-BPM/react-frontend/dist')


    # Initialize SocketIO with proper CORS support for WebSockets
    socketio = None
    if socketio_available:
        socketio = SocketIO(
            app, 
            cors_allowed_origins="*",
            async_mode="eventlet",  # Use eventlet for better WebSocket support
            ping_timeout=60,  # Increase ping timeout for stability
            engineio_logger=True,  # Enable Engine.IO logging
            json=json,  # Use the same JSON implementation
            binary=True  # Enable binary data support
        )

    
    # Enable CORS for all routes and origins
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure the Flask application
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///bpm_system.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

    # Initialize database
    from backend.models import db
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()
        
    # Make sure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Initialize extensions
    migrate = Migrate(app, db)

    # Register blueprints
    from backend.routes.admin_routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    
    from backend.routes.process_routes import bp as process_bp
    app.register_blueprint(process_bp)
    
    # Register the API blueprint which already includes gap_analysis
    from backend.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register the meeting blueprint for AI Meeting Advisor
    from backend.routes.meeting import meeting_bp, register_realtime_meeting_audio
    app.register_blueprint(meeting_bp)
    
    # Register WebSocket handlers for real-time meeting audio if available
    if socketio_available and socketio:
        register_realtime_meeting_audio(socketio)
    
    # Template download route
    @app.route('/download_template')
    def download_template():
        # Redirect to the backend route for template download
        return redirect('/api/download-template')
        
    # Serve React App
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    # Explicitly define routes for SPA navigation
    @app.route('/ai-meeting')
    @app.route('/ai-meeting/')
    def ai_meeting():
        # Force serve index.html for the AI Meeting route
        return send_from_directory(app.static_folder, 'index.html')
        
    @app.route('/evaai')
    @app.route('/evaai/')
    def evaai():
        # Force serve index.html for the EVA AI route
        return send_from_directory(app.static_folder, 'index.html')
    
    # Document processing endpoint
    @app.route('/api/process/extract', methods=['POST'])
    def extract_process_from_document():
        """Extract process from an uploaded document using OpenAI API"""
        print("=== Document upload received ===")
        
        if 'file' not in request.files:
            print("Error: No file in request")
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        print(f"File received: {file.filename}")
        
        if file.filename == '':
            print("Error: Empty filename")
            return jsonify({'error': 'No file selected'}), 400
            
        if not allowed_file(file.filename):
            print(f"Error: Invalid file format - {file.filename}")
            return jsonify({'error': f'Invalid file format. Supported formats: pdf, doc, docx'}), 400

        try:
            # Save file for processing
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            print(f"File saved to {file_path}")
            
            # For now, just return a mock response to verify the endpoint is working
            mock_process = {
                "name": f"Process from {filename}",
                "system": "Document Upload",
                "steps": [
                    {
                        "step_number": 1,
                        "description": "Upload document",
                        "approver_role": "User",
                        "approver_name": "System"
                    },
                    {
                        "step_number": 2,
                        "description": "Process document",
                        "approver_role": "System",
                        "approver_name": "AI"
                    }
                ]
            }
            
            return jsonify({
                'message': 'Document received successfully',
                'processId': 1,
                'process': mock_process
            })
                
        except Exception as e:
            print(f"General error: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': str(e)}), 500
            
    @app.route('/api/process-document', methods=['POST'])
    def process_document():
        try:
            # Check if a file was uploaded
            if 'document' not in request.files:
                logger.error("No document part in request")
                return jsonify({'error': 'No document uploaded'}), 400
            
            file = request.files['document']
            logger.info(f"Received file: {file.filename}")
            
            # Check if a file was selected
            if file.filename == '':
                logger.error("No file selected")
                return jsonify({'error': 'No file selected'}), 400
            
            # Check file type
            if not allowed_file(file.filename):
                logger.error(f"Invalid file type: {file.filename}")
                return jsonify({'error': 'Invalid file type. Please upload a PDF or Word document.'}), 400
            
            # Secure the filename and create full path
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logger.info(f"Processing file: {filename}")
            
            try:
                # Save the file
                file.save(file_path)
                logger.info(f"File saved successfully: {filename}")
                
                # Get file extension
                file_type = filename.rsplit('.', 1)[1].lower()
                
                # Process the document
                try:
                    from backend.document_processor import DocumentProcessor
                    processor = DocumentProcessor()
                    logger.info("DocumentProcessor initialized")
                    process_info_str = processor.process_document(file_path, file_type)
                    logger.info("Document processed successfully")
                    process_info = json.loads(process_info_str)
                    logger.info(f"Process info parsed: {process_info['name']}")
                except Exception as e:
                    logger.error(f"Error in document processing: {str(e)}", exc_info=True)
                    return jsonify({
                        'error': 'Failed to process document',
                        'details': str(e),
                        'type': 'processing_error'
                    }), 500
                
                try:
                    # Store in database
                    from backend.models import ERPProcess, ERPProcessStep
                    new_process = ERPProcess(
                        process_name=process_info['name'],
                        erp_system=process_info['system'],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(new_process)
                    db.session.flush()  # Get the ID without committing
                    logger.info(f"Created new process record: {new_process.id}")
                    
                    # Add steps
                    for step in process_info['steps']:
                        new_step = ERPProcessStep(
                            process_id=new_process.id,
                            step_number=step['number'],
                            step_description=step.get('description', ''),
                            approver_role=step.get('role', ''),
                            approver_name=step.get('owner', ''),
                            created_at=datetime.utcnow()
                        )
                        db.session.add(new_step)
                    
                    db.session.commit()
                    logger.info(f"Process '{process_info['name']}' saved to database with {len(process_info['steps'])} steps")
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"Database error: {str(e)}", exc_info=True)
                    return jsonify({
                        'error': 'Failed to save process to database',
                        'details': str(e),
                        'type': 'database_error'
                    }), 500
                
                try:
                    # Generate Mermaid diagram
                    mermaid_nodes = []
                    for i, step in enumerate(process_info['steps']):
                        step_number = step['number']
                        step_name = step.get('name', f'Step {step_number}')
                        step_owner = step.get('owner', 'Unassigned')
                        step_text = f"{step_number}[{step_name}<br/>{step_owner}]"
                        
                        if i < len(process_info['steps']) - 1:
                            next_step = process_info['steps'][i+1]
                            mermaid_nodes.append(f"{step_text} --> {next_step['number']}")
                        else:
                            mermaid_nodes.append(step_text)

                    mermaid_diagram = "graph TD\n" + "\n".join(mermaid_nodes)
                    logger.info("Mermaid diagram generated successfully")
                except Exception as e:
                    logger.error(f"Error generating diagram: {str(e)}", exc_info=True)
                    return jsonify({
                        'error': 'Failed to generate process diagram',
                        'details': str(e),
                        'type': 'diagram_error'
                    }), 500
                
                # Enhance response with visualization
                response_data = {
                    'process': process_info,
                    'mermaid_diagram': mermaid_diagram,
                    'message': 'Process extracted and stored successfully',
                    'analysis': {
                        'steps_count': len(process_info['steps']),
                        'manual_steps': sum(1 for step in process_info['steps'] if 'Automated' not in step.get('owner', '')),
                        'automated_steps': sum(1 for step in process_info['steps'] if 'Automated' in step.get('owner', '')),
                        'timeline': f"Approximately {len(process_info['steps']) * 2} days",
                        'key_roles': list(set(step.get('role', 'Unassigned') for step in process_info['steps']))
                    }
                }
                
                logger.info("Successfully prepared response with process analysis")
                return jsonify(response_data)
                
            except Exception as e:
                logger.error(f"Error processing document: {str(e)}", exc_info=True)
                return jsonify({
                    'error': 'Failed to process document',
                    'details': str(e),
                    'type': 'general_error'
                }), 500
                
            finally:
                # Clean up the uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up temporary file: {filename}")
        
        except Exception as e:
            logger.error(f"Unexpected error in process_document: {str(e)}", exc_info=True)
            return jsonify({
                'error': 'An unexpected error occurred',
                'details': str(e),
                'type': 'unexpected_error'
            }), 500

    @app.route('/test-document-processing')
    def test_document_processing():
        try:
            # Create a test file
            test_content = """Invoice Approval Process
System: Financial Management System
Version: 1.0

Step 1: Invoice Receipt
Description: Receive and log incoming invoice in the system
Owner: Accounts Payable Clerk
Role: Finance

Step 2: Initial Review
Description: Check invoice details, amounts, and vendor information
Owner: AP Specialist
Role: Finance"""

            # Create test PDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            for line in test_content.split('\n'):
                pdf.cell(200, 10, txt=line, ln=True)
            
            test_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test_process.pdf')
            pdf.output(test_file_path)
            logger.info(f"Created test PDF at: {test_file_path}")

            # Process the document
            from backend.document_processor import DocumentProcessor
            processor = DocumentProcessor()
            result = processor.process_document(test_file_path, 'pdf')
            
            # Clean up
            os.remove(test_file_path)
            
            return jsonify({
                'status': 'success',
                'result': json.loads(result)
            })

        except Exception as e:
            logger.error(f"Test failed: {str(e)}", exc_info=True)
            return jsonify({
                'status': 'error',
                'error': str(e),
                'type': type(e).__name__
            }), 500

    @app.route('/api/analyze-process', methods=['POST'])
    def analyze_process():
        try:
            data = request.get_json()
            process_id = data.get('process_id')
            
            if not process_id:
                return jsonify({'error': 'Process ID is required'}), 400
            
            # Get process from database
            from backend.models import ERPProcess
            process = ERPProcess.query.get(process_id)
            if not process:
                return jsonify({'error': 'Process not found'}), 404
            
            # Get all steps for the process
            from backend.models import ERPProcessStep
            steps = ERPProcessStep.query.filter_by(process_id=process_id).order_by(ERPProcessStep.step_number).all()
            
            # Format process info for analysis
            process_info = {
                'name': process.process_name,
                'system': process.erp_system,
                'version': '1.0',  # You might want to add version tracking to your model
                'steps': [{
                    'number': step.step_number,
                    'name': f'Step {step.step_number}',
                    'description': step.step_description,
                    'owner': step.approver_name,
                    'role': step.approver_role
                } for step in steps]
            }
            
            # Initialize process analyzer
            from backend.process_analyzer import ProcessAnalyzer
            from backend.openai_api import OpenAI
            analyzer = ProcessAnalyzer(OpenAI(api_key=os.getenv('OPENAI_API_KEY')))
            
            # Get analysis
            analysis = analyzer.analyze_process(process_info)
            
            return jsonify(analysis)
            
        except Exception as e:
            logger.error(f"Error analyzing process: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/list-process-versions', methods=['POST'])
    def list_process_versions():
        try:
            data = request.get_json()
            process_name = data.get('process_name')
            
            if not process_name:
                return jsonify({'error': 'Process name is required'}), 400
            
            # Get all versions of the process
            from backend.models import ERPProcess
            versions = ERPProcess.query.filter_by(process_name=process_name)\
                .order_by(ERPProcess.created_at.desc()).all()
            
            return jsonify([{
                'id': version.id,
                'version': '1.0',  # You might want to add version tracking
                'created_at': version.created_at.isoformat(),
                'updated_at': version.updated_at.isoformat()
            } for version in versions])
            
        except Exception as e:
            logger.error(f"Error listing process versions: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/compare-processes', methods=['POST'])
    def compare_processes():
        try:
            data = request.get_json()
            current_process_id = data.get('current_process_id')
            compare_process_id = data.get('compare_process_id')
            
            if not current_process_id or not compare_process_id:
                return jsonify({'error': 'Both process IDs are required'}), 400
            
            # Get both processes
            from backend.models import ERPProcess
            current_process = ERPProcess.query.get(current_process_id)
            compare_process = ERPProcess.query.get(compare_process_id)
            
            if not current_process or not compare_process:
                return jsonify({'error': 'One or both processes not found'}), 404
            
            # Get steps for both processes
            from backend.models import ERPProcessStep
            current_steps = ERPProcessStep.query.filter_by(process_id=current_process_id)\
                .order_by(ERPProcessStep.step_number).all()
            compare_steps = ERPProcessStep.query.filter_by(process_id=compare_process_id)\
                .order_by(ERPProcessStep.step_number).all()
            
            # Format process info for comparison
            current_info = {
                'name': current_process.process_name,
                'system': current_process.erp_system,
                'version': '1.0',
                'steps': [{
                    'number': step.step_number,
                    'name': f'Step {step.step_number}',
                    'description': step.step_description,
                    'owner': step.approver_name,
                    'role': step.approver_role
                } for step in current_steps]
            }
            
            compare_info = {
                'name': compare_process.process_name,
                'system': compare_process.erp_system,
                'version': '1.0',
                'steps': [{
                    'number': step.step_number,
                    'name': f'Step {step.step_number}',
                    'description': step.step_description,
                    'owner': step.approver_name,
                    'role': step.approver_role
                } for step in compare_steps]
            }
            
            # Initialize process analyzer
            from backend.process_analyzer import ProcessAnalyzer
            from backend.openai_api import OpenAI
            analyzer = ProcessAnalyzer(OpenAI(api_key=os.getenv('OPENAI_API_KEY')))
            
            # Get comparison
            comparison = analyzer.compare_processes(current_info, compare_info)
            
            return jsonify(comparison)
            
        except Exception as e:
            logger.error(f"Error comparing processes: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    # Return both app and socketio
    if socketio_available and socketio:
        return app, socketio
    return app, None

if __name__ == '__main__':
    app, socketio = create_app()
    if socketio_available and socketio:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
