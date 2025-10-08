# AI-Powered Business Process Management System

An intelligent system for extracting, analyzing, and optimizing business processes using AI.

## Features

- Extract business processes from PDF/Word documents
- AI-powered gap analysis and optimization
- Best practices recommendations
- Interactive workflow diagrams
- Process comparison and versioning

## Tech Stack

- Frontend: React.js
- Backend: Flask
- AI Processing: OpenAI GPT-4
- Workflow Visualization: Mermaid.js
- Database: SQLite (Development) / PostgreSQL (Production)

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configurations
```

4. Run the Flask application:
```bash
flask run
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Endpoints

- `POST /api/extract-process`: Extract process from document
- `POST /api/analyze-process`: Analyze and get recommendations
- `POST /api/generate-workflow`: Generate workflow diagram

## Development

- Backend runs on: http://localhost:5000
- Frontend runs on: http://localhost:3000

## Testing

```bash
# Run backend tests
cd backend
pytest

# Run frontend tests
cd frontend
npm test
```
