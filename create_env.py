# Script to create a proper UTF-8 encoded .env file
import os

# Get the absolute path for the database
app_dir = os.path.dirname(os.path.abspath(__file__))
instance_dir = os.path.join(app_dir, 'instance')
db_path = os.path.join(instance_dir, 'bpm_system.db')

# Make sure instance directory exists
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir)
    print(f"Created instance directory at {instance_dir}")

with open('.env', 'w', encoding='utf-8') as f:
    f.write(f"""FLASK_APP=wsgi.py
FLASK_ENV=development
DATABASE_URL=sqlite:///{db_path}
SECRET_KEY=your-secure-secret-key
OPENAI_API_KEY=your-openai-api-key
ALLOWED_ORIGINS=http://localhost:5000
""")
    
print(".env file created successfully with UTF-8 encoding")
print(f"Database path set to: {db_path}")
