@echo off
echo 🐍 Setting up Resume Analyzer with Python 3.10
echo ================================================

echo.
echo 1. Checking Python 3.10 installation...
py -3.10 --version
if %errorlevel% neq 0 (
    echo ❌ Python 3.10 not found with py launcher
    echo Trying alternative methods...
    python3.10 --version
    if %errorlevel% neq 0 (
        echo ❌ Python 3.10 not accessible
        echo Please ensure Python 3.10 is installed and accessible
        pause
        exit /b 1
    )
    set PYTHON_CMD=python3.10
) else (
    set PYTHON_CMD=py -3.10
)

echo ✅ Found Python 3.10!

echo.
echo 2. Creating virtual environment with Python 3.10...
%PYTHON_CMD% -m venv venv_py310
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo 3. Activating virtual environment...
call venv_py310\Scripts\activate.bat

echo.
echo 4. Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 5. Installing requirements for Python 3.10...
pip install -r requirements_py310.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install requirements
    echo Trying with trusted hosts...
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements_py310.txt
    if %errorlevel% neq 0 (
        echo ❌ Installation failed even with trusted hosts
        pause
        exit /b 1
    )
)

echo.
echo 6. Downloading spaCy language model...
python -m spacy download en_core_web_sm
if %errorlevel% neq 0 (
    echo ❌ Failed to download spaCy model
    echo Trying alternative method...
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
    if %errorlevel% neq 0 (
        echo ❌ Failed to install spaCy model
        pause
        exit /b 1
    )
)

echo.
echo 7. Testing installation...
python -c "
import sys
print(f'Python version: {sys.version}')
try:
    import spacy
    print(f'✅ spaCy version: {spacy.__version__}')
except ImportError as e:
    print(f'❌ spaCy import failed: {e}')
    exit(1)

try:
    import sentence_transformers
    print(f'✅ sentence-transformers version: {sentence_transformers.__version__}')
except ImportError as e:
    print(f'❌ sentence-transformers import failed: {e}')
    exit(1)

try:
    import flask
    print(f'✅ Flask version: {flask.__version__}')
except ImportError as e:
    print(f'❌ Flask import failed: {e}')
    exit(1)

print('✅ All critical packages imported successfully!')
"

if %errorlevel% neq 0 (
    echo ❌ Installation test failed
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete with Python 3.10! 
echo.
echo 🚀 To start the application:
echo    1. Activate environment: venv_py310\Scripts\activate
echo    2. Run server: python app.py
echo    3. Open browser: http://localhost:5000
echo.
echo 🧪 To test the setup: python check_python.py
echo.
pause