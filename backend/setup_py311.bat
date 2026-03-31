@echo off
echo 🐍 Setting up Resume Analyzer with Python 3.11
echo ================================================

echo.
echo 1. Checking Python 3.11 installation...
python3.11 --version
if %errorlevel% neq 0 (
    echo ❌ Python 3.11 not found. Please install Python 3.11 from python.org
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo 2. Creating virtual environment...
python3.11 -m venv venv_py311
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo 3. Activating virtual environment...
call venv_py311\Scripts\activate.bat

echo.
echo 4. Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 5. Installing requirements...
pip install -r requirements_py311.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    pause
    exit /b 1
)

echo.
echo 6. Downloading spaCy language model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo ❌ Failed to download spaCy model
    pause
    exit /b 1
)

echo.
echo 7. Testing installation...
python -c "
import spacy
import sentence_transformers
import flask
print('✅ All packages imported successfully!')
print(f'Python version: {__import__('sys').version}')
print(f'spaCy version: {spacy.__version__}')
print(f'sentence-transformers version: {sentence_transformers.__version__}')
print(f'Flask version: {flask.__version__}')
"

if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete! 
echo.
echo 🚀 To start the application:
echo    1. Activate environment: venv_py311\Scripts\activate
echo    2. Run server: python app.py
echo    3. Open browser: http://localhost:5000
echo.
pause