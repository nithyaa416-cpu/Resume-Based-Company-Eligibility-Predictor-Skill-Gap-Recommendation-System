#!/usr/bin/env python3
"""
Dependency Checker for Resume Analysis System
Checks which features are available based on installed packages
"""

import sys

def check_dependency(module_name, package_name=None):
    """Check if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        return True, f"✓ {package_name} is installed"
    except ImportError:
        return False, f"✗ {package_name} is NOT installed"

def main():
    print("=" * 60)
    print("Resume Analysis System - Dependency Check")
    print("=" * 60)
    print()
    
    # Core dependencies
    print("CORE DEPENDENCIES (Required for basic features):")
    print("-" * 60)
    
    core_deps = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('PyPDF2', 'PyPDF2'),
        ('docx', 'python-docx'),
        ('nltk', 'NLTK'),
        ('sklearn', 'scikit-learn'),
        ('spacy', 'spaCy'),
        ('numpy', 'NumPy'),
        ('torch', 'PyTorch'),
        ('transformers', 'Transformers'),
    ]
    
    core_ok = True
    for module, name in core_deps:
        ok, msg = check_dependency(module, name)
        print(f"  {msg}")
        if not ok:
            core_ok = False
    
    print()
    
    # Enhanced features dependencies
    print("ENHANCED FEATURES DEPENDENCIES (Optional):")
    print("-" * 60)
    
    enhanced_deps = [
        ('jwt', 'PyJWT - for authentication'),
        ('bcrypt', 'bcrypt - for password hashing'),
        ('cryptography', 'cryptography - for security'),
        ('pandas', 'pandas - for data analysis'),
        ('joblib', 'joblib - for ML caching'),
        ('scipy', 'scipy - for advanced ML'),
    ]
    
    enhanced_ok = True
    for module, name in enhanced_deps:
        ok, msg = check_dependency(module, name)
        print(f"  {msg}")
        if not ok:
            enhanced_ok = False
    
    print()
    print("=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    
    if core_ok:
        print("✓ Core features: AVAILABLE")
        print("  - Resume upload and analysis")
        print("  - Company matching")
        print("  - ML eligibility scoring")
        print("  - ATS analysis")
        print("  - Resume optimization")
    else:
        print("✗ Core features: MISSING DEPENDENCIES")
        print("  Run: pip install -r requirements.txt")
    
    print()
    
    if enhanced_ok:
        print("✓ Enhanced features: AVAILABLE")
        print("  - User authentication")
        print("  - Resume history tracking")
        print("  - Interview preparation")
        print("  - Mobile app support")
    else:
        print("⚠ Enhanced features: MISSING DEPENDENCIES")
        print("  Run: install_enhanced_features.bat (Windows)")
        print("  Or:  ./install_enhanced_features.sh (Linux/Mac)")
        print("  Or:  pip install PyJWT bcrypt cryptography pandas joblib scipy")
    
    print()
    print("=" * 60)
    
    # Return exit code
    if not core_ok:
        print("\n⚠ WARNING: Core dependencies missing. App may not start.")
        return 1
    elif not enhanced_ok:
        print("\n✓ App will start with basic features only.")
        return 0
    else:
        print("\n✓ All features available!")
        return 0

if __name__ == "__main__":
    sys.exit(main())