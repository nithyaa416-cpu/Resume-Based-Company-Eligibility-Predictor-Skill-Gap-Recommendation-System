# Setup Guide - Resume-Based Company Eligibility System

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- SQLite (usually comes with Python)

## Installation Steps

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

If you encounter any issues, install packages individually:
```bash
pip install Flask==2.3.3
pip install Flask-CORS==4.0.0
pip install PyPDF2==3.0.1
pip install python-docx==0.8.11
pip install nltk==3.8.1
pip install scikit-learn==1.3.0
```

### 4. Download NLTK Data
Run Python and execute:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

Or run this one-time setup script:
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 5. Verify Database
Make sure your `database/jobs.db` file exists and contains data. If not, run:
```bash
cd database
python create_db.py
python insert_data.py
```

### 6. Test the System
Run the test script to verify everything works:
```bash
python test_system.py
```

### 7. Start the Flask Server
```bash
python app.py
```

The server should start on `http://localhost:5000`

## Verification

### Test Basic Functionality
1. **Check if server is running:**
   - Open browser and go to `http://localhost:5000`
   - You should see a JSON response with system information

2. **Test companies endpoint:**
   - Go to `http://localhost:5000/companies`
   - You should see a list of companies

3. **Test file upload:**
   - Use a tool like Postman or curl to upload a resume file
   - Or use the provided test script

## Project Structure

After setup, your backend structure should look like:

```
backend/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── test_system.py        # Test script
├── API_DOCUMENTATION.md  # API documentation
├── SETUP_GUIDE.md       # This file
├── database/
│   ├── jobs.db          # SQLite database
│   ├── db_utils.py      # Database utilities
│   ├── create_db.py     # Database creation script
│   ├── insert_data.py   # Data insertion script
│   └── __init__.py
├── utils/
│   ├── resume_parser.py      # Resume parsing utilities
│   ├── skill_extractor.py    # Skill extraction logic
│   ├── eligibility_calculator.py # Eligibility calculation
│   └── __init__.py
└── venv/                # Virtual environment (if created)
```

## Troubleshooting

### Common Issues

1. **Import Errors:**
   - Make sure you're in the backend directory
   - Ensure virtual environment is activated
   - Verify all packages are installed

2. **Database Errors:**
   - Check if `database/jobs.db` exists
   - Verify database has data by running test script
   - Re-run database creation scripts if needed

3. **File Upload Errors:**
   - Ensure uploaded files are PDF or DOCX format
   - Check file size (should be under 10MB)
   - Verify file is not corrupted

4. **NLTK Errors:**
   - Run the NLTK download commands again
   - Check internet connection during NLTK downloads

5. **Port Already in Use:**
   - Change port in app.py: `app.run(debug=True, port=5001)`
   - Or kill the process using port 5000

### Testing Individual Components

1. **Test Database:**
```bash
python -c "from database.db_utils import get_all_companies; print(get_all_companies())"
```

2. **Test Skill Extraction:**
```bash
python -c "from utils.skill_extractor import SkillExtractor; se = SkillExtractor(); print(se.extract_all_skills_flat('I know Python and Java'))"
```

3. **Test Resume Parser:**
```bash
# Create a test text file and test
echo "Test resume content" > test.txt
python -c "from utils.resume_parser import ResumeParser; print('Parser loaded successfully')"
```

## Next Steps

Once the backend is running successfully:

1. **Test all API endpoints** using the API documentation
2. **Create sample resume files** for testing
3. **Plan the React frontend** structure
4. **Consider additional features** like user authentication, resume storage, etc.

## Development Tips

1. **Use virtual environment** to avoid package conflicts
2. **Keep the server running** during development for testing
3. **Check logs** in the terminal for debugging
4. **Use Postman or similar tools** for API testing
5. **Backup your database** before making changes

## Production Considerations

For production deployment, consider:
- Using a production WSGI server (like Gunicorn)
- Setting up proper logging
- Adding input validation and security measures
- Using environment variables for configuration
- Setting up proper error handling