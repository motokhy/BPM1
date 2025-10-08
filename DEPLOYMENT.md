# AI-Powered BPM System Deployment Guide

## Prerequisites

### System Requirements
- Python 3.8+
- PostgreSQL 13+
- Node.js 16+ (for frontend)
- OpenAI API key
- SSL certificate

### Environment Variables
```
FLASK_APP=wsgi.py
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost:5432/bpm_db
SECRET_KEY=your-secure-secret-key
OPENAI_API_KEY=your-openai-api-key
ALLOWED_ORIGINS=https://your-domain.com
```

## Quick Deploy to Render.com (Free Tier)

1. Create a Render Account:
   - Go to [Render.com](https://render.com)
   - Sign up for a free account

2. Fork/Push Your Repository:
   - Push your code to a GitHub repository
   - Make sure all files are committed:
     - app.py
     - wsgi.py
     - requirements.txt
     - render.yaml
     - gunicorn.conf.py

3. Create New Web Service:
   - Click "New +" in Render dashboard
   - Select "Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the Python application

4. Configure Environment Variables:
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your-api-key
     ```
   - Render will automatically generate and set:
     - DATABASE_URL
     - SECRET_KEY

5. Deploy:
   - Click "Create Web Service"
   - Render will automatically:
     - Create a PostgreSQL database
     - Deploy your application
     - Run migrations
     - Start the service

Your application will be available at: `https://ai-powered-bpm.onrender.com`

## Database Setup

1. Install PostgreSQL:
```bash
# Ubuntu
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Windows
# Download and install from https://www.postgresql.org/download/windows/
```

2. Create Database:
```sql
CREATE DATABASE bpm_db;
```

3. Run Migrations:
```bash
flask db upgrade
```

## Application Deployment

### Backend Setup

1. Clone Repository:
```bash
git clone <repository-url>
cd AI-Powered-BPM
```

2. Install Dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Linux
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

3. Initialize Database:
```bash
flask db upgrade
```

4. Configure Gunicorn (Linux):
```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

### Frontend Setup

1. Install Dependencies:
```bash
cd frontend
npm install
```

2. Build Production Assets:
```bash
npm run build
```

## Security Configuration

1. SSL Setup:
   - Obtain SSL certificate
   - Configure web server for HTTPS

2. Firewall Rules:
   - Allow ports 80/443 for web traffic
   - Restrict database port access
   - Configure application-specific ports

## Monitoring Setup

1. Configure Logging:
   - Set up application logging
   - Configure error tracking
   - Enable audit logging

2. Set up Monitoring:
   - Configure system monitoring
   - Set up performance monitoring
   - Enable error alerting

## Backup Strategy

1. Database Backups:
```bash
# Daily backup script
pg_dump -U postgres bpm_db > backup_$(date +%Y%m%d).sql
```

2. Document Storage Backups:
   - Configure regular backups of uploaded documents
   - Set up backup rotation policy

## Post-Deployment Verification

1. Check System Status:
   - Verify all services are running
   - Test database connectivity
   - Validate API endpoints
   - Check document processing

2. Security Verification:
   - Verify SSL configuration
   - Test authentication
   - Validate file upload restrictions
   - Check API rate limiting

## Troubleshooting

Common issues and solutions:

1. Database Connection Issues:
   - Check PostgreSQL service status
   - Verify connection string
   - Check network connectivity

2. Document Processing Issues:
   - Verify OpenAI API key
   - Check file permissions
   - Validate upload directory

3. Performance Issues:
   - Check server resources
   - Monitor database performance
   - Review application logs

## Maintenance

Regular maintenance tasks:

1. Database:
   - Regular vacuum operations
   - Index maintenance
   - Performance optimization

2. Application:
   - Log rotation
   - Cache clearing
   - Security updates

3. System:
   - OS updates
   - Dependency updates
   - SSL certificate renewal
