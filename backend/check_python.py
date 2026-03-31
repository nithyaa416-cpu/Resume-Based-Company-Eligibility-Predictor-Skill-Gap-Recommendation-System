"""
Check Python Version Compatibility
This script checks if you have a compatible Python version for the ML features
"""

import sys
import subprocess
import os

def check_python_version():
    print("🐍 PYTHON VERSION COMPATIBILITY CHECK")
    print("=" * 50)
    
    current_version = sys.version_info
    print(f"Current Python version: {current_version.major}.{current_version.minor}.{current_version.micro}")
    
    # Check if current version is compatible
    if current_version.major == 3 and current_version.minor in [10, 11]:
        print("✅ Current Python version is compatible!")
        return True
    elif current_version.major == 3 and current_version.minor >= 12:
        print("⚠️ Python 3.12+ detected - spaCy compatibility issues may occur")
        print("Recommended: Use Python 3.10 or 3.11")
        return False
    else:
        print("❌ Incompatible Python version")
        print("Required: Python 3.10 or 3.11")
        return False

def check_available_pythons():
    print("\n🔍 CHECKING AVAILABLE PYTHON VERSIONS")
    print("-" * 40)
    
    python_versions = ['python3.11', 'python3.10', 'python', 'py -3.11', 'py -3.10']
    available = []
    
    for py_cmd in python_versions:
        try:
            if py_cmd.startswith('py -'):
                # Windows py launcher
                result = subprocess.run(py_cmd.split(), capture_output=True, text=True, timeout=5)
            else:
                result = subprocess.run([py_cmd, '--version'], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                version_info = result.stdout.strip() or result.stderr.strip()
                print(f"✅ {py_cmd}: {version_info}")
                available.append((py_cmd, version_info))
            else:
                print(f"❌ {py_cmd}: Not available")
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            print(f"❌ {py_cmd}: Not available")
    
    return available

def test_imports():
    print("\n🧪 TESTING CRITICAL IMPORTS")
    print("-" * 30)
    
    imports_to_test = [
        ('flask', 'Flask'),
        ('spacy', 'spaCy'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('sklearn', 'Scikit-learn')
    ]
    
    all_good = True
    
    for module, name in imports_to_test:
        try:
            __import__(module)
            print(f"✅ {name}: Available")
        except ImportError as e:
            print(f"❌ {name}: Missing - {e}")
            all_good = False
    
    return all_good

def main():
    print("🤖 RESUME ANALYZER - PYTHON COMPATIBILITY CHECK")
    print("=" * 60)
    
    # Check current Python version
    current_compatible = check_python_version()
    
    # Check available Python versions
    available_pythons = check_available_pythons()
    
    # Test imports if current version is compatible
    if current_compatible:
        imports_ok = test_imports()
    else:
        imports_ok = False
    
    print("\n📋 SUMMARY")
    print("-" * 20)
    
    if current_compatible and imports_ok:
        print("🎉 Everything looks good! You can run the application.")
        print("\n🚀 Next steps:")
        print("1. Run: python app.py")
        print("2. Open: http://localhost:5000")
    
    elif current_compatible and not imports_ok:
        print("⚠️ Python version is compatible but packages are missing.")
        print("\n🔧 Next steps:")
        print("1. Install requirements: pip install -r requirements_py311.txt")
        print("2. Download spaCy model: python -m spacy download en_core_web_sm")
    
    else:
        print("❌ Python version incompatible or packages missing.")
        print("\n🔧 Recommended solutions:")
        
        # Find best available Python
        compatible_pythons = []
        for py_cmd, version_info in available_pythons:
            if '3.11' in version_info or '3.10' in version_info:
                compatible_pythons.append((py_cmd, version_info))
        
        if compatible_pythons:
            print("✅ Compatible Python versions found:")
            for py_cmd, version_info in compatible_pythons:
                print(f"   Use: {py_cmd}")
                print(f"   Setup: {py_cmd} -m venv venv && venv\\Scripts\\activate && pip install -r requirements_py311.txt")
        else:
            print("📥 Install Python 3.11:")
            print("   Download from: https://www.python.org/downloads/")
            print("   Or use setup script: setup_py311.bat (Windows) or setup_py311.sh (Linux/Mac)")
    
    print("\n📚 For detailed setup instructions, see: PYTHON_VERSION_SETUP.md")

if __name__ == "__main__":
    main()