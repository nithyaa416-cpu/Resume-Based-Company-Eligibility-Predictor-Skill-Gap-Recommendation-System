# 🐍 Python Version Setup Guide

## ⚠️ Important: Python 3.14 Compatibility Issue

**Problem**: Python 3.14 doesn't support spaCy, which is required for our ML/NLP features.

**Solution**: Use Python 3.10 or 3.11 (recommended: Python 3.11)

## 🔧 Setup Options

### Option 1: Install Python 3.11 (Recommended)

1. **Download Python 3.11**:
   - Go to: https://www.python.org/downloads/
   - Download Python 3.11.x (latest stable)
   - Install with "Add to PATH" checked

2. **Verify Installation**:
   ```bash
   python3.11 --version
   # Should show: Python 3.11.x
   ```

3. **Create Virtual Environment**:
   ```bash
   cd backend
   python3.11 -m venv venv_py311
   ```

4. **Activate Virtual Environment**:
   ```bash
   # Windows
   venv_py311\Scripts\activate
   
   # Linux/Mac
   source venv_py311/bin/activate
   ```

5. **Install Requirements**:
   ```bash
   pip install -r requirements_py311.txt
   ```

### Option 2: Use pyenv (Advanced Users)

1. **Install pyenv**:
   ```bash
   # Windows (using chocolatey)
   choco install pyenv-win
   
   # Or download from: https://github.com/pyenv-win/pyenv-win
   ```

2. **Install Python 3.11**:
   ```bash
   pyenv install 3.11.7
   pyenv local 3.11.7
   ```

3. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements_py311.txt
   ```

### Option 3: Use Conda

1. **Install Miniconda/Anaconda**

2. **Create Environment**:
   ```bash
   conda create -n resume_analyzer python=3.11
   conda activate resume_analyzer
   pip install -r requirements_py311.txt
   ```

## 📦 Updated Requirements

I'll create a Python 3.11 compatible requirements file:

### requirements_py311.txt
```
Flask==2.3.3
Flask-CORS==4.0.0
sentence-transformers==2.2.2
spacy==3.7.2
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2
PyPDF2==3.0.1
python-docx==0.8.11
requests==2.31.0
```

## 🚀 Quick Start with Python 3.11

1. **Install Python 3.11** from python.org
2. **Create project directory**:
   ```bash
   cd your_project_folder/backend
   ```
3. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv_py311
   venv_py311\Scripts\activate  # Windows
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements_py311.txt
   python -m spacy download en_core_web_sm
   ```
5. **Run the application**:
   ```bash
   python app.py
   ```

## 🔍 Verify Setup

Run this test to verify everything works:

```bash
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
```

## 🐛 Troubleshooting

### If spaCy installation fails:
```bash
pip install --upgrade pip
pip install spacy==3.7.2
python -m spacy download en_core_web_sm
```

### If sentence-transformers fails:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install sentence-transformers==2.2.2
```

### If you get SSL errors:
```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements_py311.txt
```

## ✅ Success Indicators

You'll know the setup is working when:
- `python --version` shows 3.10.x or 3.11.x
- `python app.py` starts without import errors
- You see: "ML Models: Sentence-BERT (all-MiniLM-L6-v2), spaCy NLP"
- The web interface loads at http://localhost:5000

## 🎯 Next Steps

After successful setup:
1. Run `python app.py` in the backend folder
2. Open http://localhost:5000
3. Test with the sample resume from the troubleshooting guide
4. Verify all ML features are working

The system will work perfectly with Python 3.11!