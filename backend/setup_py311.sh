#!/bin/bash

echo "🐍 Setting up Resume Analyzer with Python 3.11"
echo "================================================"

echo ""
echo "1. Checking Python 3.11 installation..."
if ! command -v python3.11 &> /dev/null; then
    echo "❌ Python 3.11 not found. Please install Python 3.11"
    echo "Ubuntu/Debian: sudo apt install python3.11 python3.11-venv"
    echo "macOS: brew install python@3.11"
    echo "Or download from: https://www.python.org/downloads/"
    exit 1
fi

python3.11 --version

echo ""
echo "2. Creating virtual environment..."
python3.11 -m venv venv_py311
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo ""
echo "3. Activating virtual environment..."
source venv_py311/bin/activate

echo ""
echo "4. Upgrading pip..."
python -m pip install --upgrade pip

echo ""
echo "5. Installing requirements..."
pip install -r requirements_py311.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install requirements"
    exit 1
fi

echo ""
echo "6. Downloading spaCy language model..."
python -m spacy download en_core_web_sm
if [ $? -ne 0 ]; then
    echo "❌ Failed to download spaCy model"
    exit 1
fi

echo ""
echo "7. Testing installation..."
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

if [ $? -ne 0 ]; then
    echo "❌ Installation test failed"
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   1. Activate environment: source venv_py311/bin/activate"
echo "   2. Run server: python app.py"
echo "   3. Open browser: http://localhost:5000"
echo ""