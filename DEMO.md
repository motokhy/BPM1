# AI-Powered BPM System Demo Guide

## Prerequisites
- Python 3.8+
- PostgreSQL
- Node.js 14+

## Quick Start

1. Clone the repository
2. Set up the environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure the database:
- Create a PostgreSQL database
- Update `.env` file with your database credentials

4. Set up the frontend:
```bash
cd frontend
npm install
npm run build
```

5. Initialize the database:
```bash
flask db upgrade
python setup_demo_data.py
```

6. Run the application:
```bash
python run.py
```

Visit http://localhost:5000 to access the application.

## Demo Credentials
- Username: demo@example.com
- Password: demo123

## Sample Processes
The demo includes pre-loaded sample processes:
1. Purchase Order Approval
2. Employee Onboarding
3. Invoice Processing

## Key Features Demo

### 1. Document Processing
- Upload the sample PO document from `demo/samples/purchase_order.pdf`
- Watch as the system extracts the workflow automatically
- View the generated process map

### 2. Process Analysis
- Navigate to the "Analysis" tab
- View AI-generated optimization suggestions
- Compare with best practices

### 3. Process Visualization
- Interactive workflow diagrams
- Version comparison
- Process optimization recommendations

### 4. Best Practices Library
- Access pre-loaded industry best practices
- Compare your processes with standards
- View improvement suggestions

## Demo Tips
- Use the sample documents in `demo/samples/` for best results
- Explore the version control feature by making process modifications
- Try the gap analysis feature with different processes
