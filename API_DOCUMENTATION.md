# AI-Powered BPM System API Documentation

## Overview

This API powers an AI-driven Business Process Management system that helps organizations optimize their business processes through:
- Document processing (PDF/Word)
- AI-powered workflow extraction
- Gap analysis and optimization
- Best practices recommendations
- Process versioning and visualization

## Base URL
```
Production: https://your-domain.com/api
Development: http://localhost:5000/api
```

## Authentication

All API requests require an authentication token in the header:
```
Authorization: Bearer <your-token>
```

## Endpoints

### 1. Document Management

#### Upload Document
```http
POST /documents
Content-Type: multipart/form-data

Parameters:
- file: PDF or Word document (Required)

Response: 201 Created
{
    "document": {
        "id": "uuid",
        "filename": "process.pdf",
        "file_type": "pdf",
        "created_at": "2025-03-08T05:38:46+02:00",
        "status": "uploaded"
    }
}
```

#### List Documents
```http
GET /documents

Query Parameters:
- page: int (Optional, default=1)
- per_page: int (Optional, default=10)
- file_type: string (Optional, "pdf" or "docx")

Response: 200 OK
{
    "documents": [{
        "id": "uuid",
        "filename": "process.pdf",
        "file_type": "pdf",
        "created_at": "2025-03-08T05:38:46+02:00",
        "status": "processed"
    }],
    "total": 100,
    "page": 1,
    "per_page": 10
}
```

### 2. Workflow Processing

#### Extract Workflow
```http
POST /workflows/extract/{document_id}

Response: 201 Created
{
    "workflow": {
        "id": "uuid",
        "name": "Purchase Order Process",
        "status": "extracted",
        "mermaid_diagram": "graph TD...",
        "steps": [{
            "id": 1,
            "name": "Submit Request",
            "type": "start",
            "next_steps": [2]
        }]
    }
}
```

#### Analyze Workflow
```http
POST /workflows/{workflow_id}/analyze

Response: 200 OK
{
    "analysis": {
        "gaps_identified": [{
            "id": 1,
            "description": "Missing validation step",
            "severity": "high",
            "recommendation": "Add input validation"
        }],
        "risk_assessment": [{
            "id": 1,
            "description": "No approval step",
            "impact": "high",
            "mitigation": "Add manager approval"
        }],
        "compliance_issues": [{
            "id": 1,
            "standard": "SOX",
            "description": "Audit trail required"
        }]
    }
}
```

#### Get Optimization Recommendations
```http
POST /workflows/{workflow_id}/optimize

Response: 200 OK
{
    "optimization": {
        "recommendations": [{
            "id": 1,
            "description": "Add validation step",
            "impact": "Reduces errors by 50%",
            "priority": "high"
        }],
        "best_practices": [{
            "id": 1,
            "category": "Security",
            "description": "Implement role-based access"
        }],
        "optimized_diagram": "graph TD..."
    }
}
```

### 3. ERP Process Management

#### Create ERP Process
```http
POST /erp-processes
Content-Type: application/json

Request Body:
{
    "process_name": "Purchase Order Approval",
    "erp_system": "SAP",
    "steps": [{
        "step_number": 1,
        "step_description": "Create PO",
        "approver_role": "Manager",
        "approver_name": "John Doe"
    }]
}

Response: 201 Created
{
    "process": {
        "id": "uuid",
        "process_name": "Purchase Order Approval",
        "erp_system": "SAP",
        "created_at": "2025-03-08T05:38:46+02:00",
        "steps": [...]
    }
}
```

#### List ERP Processes
```http
GET /erp-processes

Query Parameters:
- erp_system: string (Optional)
- process_name: string (Optional, search term)
- page: int (Optional, default=1)
- per_page: int (Optional, default=10)

Response: 200 OK
{
    "processes": [{
        "id": "uuid",
        "process_name": "Purchase Order Approval",
        "erp_system": "SAP",
        "created_at": "2025-03-08T05:38:46+02:00",
        "steps_count": 5
    }],
    "total": 50,
    "page": 1,
    "per_page": 10
}
```

## Error Responses

### Common Error Codes
```json
400 Bad Request
{
    "error": "Invalid request parameters",
    "details": "File type not supported"
}

401 Unauthorized
{
    "error": "Authentication failed",
    "details": "Invalid or expired token"
}

404 Not Found
{
    "error": "Resource not found",
    "details": "Document with id 'uuid' not found"
}

500 Internal Server Error
{
    "error": "Internal server error",
    "details": "Database connection failed"
}
```

## Rate Limiting

- Rate limit: 100 requests per minute per IP
- Rate limit headers included in responses:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset

## Best Practices

1. **Error Handling**
   - Always check response status codes
   - Handle rate limiting appropriately
   - Implement exponential backoff for retries

2. **File Upload**
   - Maximum file size: 10MB
   - Supported formats: PDF, DOCX
   - Use multipart/form-data for uploads

3. **Authentication**
   - Store tokens securely
   - Refresh tokens before expiration
   - Include token in all requests

4. **Performance**
   - Use pagination for list endpoints
   - Cache frequently accessed data
   - Compress large responses
