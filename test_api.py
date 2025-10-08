import requests
import json
import os

BASE_URL = 'http://localhost:5000/api'

def test_document_upload():
    """Test document upload endpoint"""
    # Use our sample process document
    pdf_path = 'tests/data/sample_process.txt'
    
    with open(pdf_path, 'rb') as f:
        files = {'file': ('sample_process.txt', f)}
        response = requests.post(f'{BASE_URL}/documents', files=files)
        
    print('Document Upload Test:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    return response.json().get('document', {}).get('id')

def test_workflow_extraction(document_id):
    """Test workflow extraction endpoint"""
    response = requests.post(f'{BASE_URL}/workflows/extract/{document_id}')
    
    print('\nWorkflow Extraction Test:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
    return response.json().get('workflow', {}).get('id')

def test_workflow_analysis(workflow_id):
    """Test workflow analysis endpoint"""
    response = requests.post(f'{BASE_URL}/workflows/{workflow_id}/analyze')
    
    print('\nWorkflow Analysis Test:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')

def test_workflow_optimization(workflow_id):
    """Test workflow optimization endpoint"""
    response = requests.post(f'{BASE_URL}/workflows/{workflow_id}/optimize')
    
    print('\nWorkflow Optimization Test:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')

def test_erp_process_creation():
    """Test ERP process creation endpoint"""
    data = {
        "process_name": "Invoice Processing",
        "erp_system": "SAP",
        "steps": [
            {
                "step_number": 1,
                "step_description": "Receive Invoice",
                "approver_role": "AP Clerk",
                "approver_name": "Jane Smith"
            }
        ]
    }
    
    response = requests.post(
        f'{BASE_URL}/erp-processes',
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print('\nERP Process Creation Test:')
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')

def run_all_tests():
    """Run all API tests in sequence"""
    try:
        # Start with document upload
        document_id = test_document_upload()
        if document_id:
            # Extract workflow
            workflow_id = test_workflow_extraction(document_id)
            if workflow_id:
                # Analyze and optimize workflow
                test_workflow_analysis(workflow_id)
                test_workflow_optimization(workflow_id)
        
        # Test ERP process
        test_erp_process_creation()
        
    except requests.exceptions.RequestException as e:
        print(f'\nError occurred: {e}')
    except Exception as e:
        print(f'\nUnexpected error: {e}')

if __name__ == '__main__':
    # Make sure the Flask server is running before executing tests
    run_all_tests()
