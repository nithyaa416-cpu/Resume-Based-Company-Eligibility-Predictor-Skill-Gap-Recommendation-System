# Quick Fix Guide - JSON Error

## Problem
You're seeing: "Error loading companies: Unexpected token '<', "<!doctype "... is not valid JSON"

## Root Cause
The Flask backend is crashing on startup because the new enhanced features require additional dependencies that aren't installed yet.

## Solution

### Option 1: Install Enhanced Features (Recommended)

**Windows:**
```bash
cd resume/backend
install_enhanced_features.bat
```

**Linux/Mac:**
```bash
cd resume/backend
chmod +x install_enhanced_features.sh
./install_enhanced_features.sh
```

**Or manually:**
```bash
pip install PyJWT==2.8.0 bcrypt==4.0.1 cryptography==41.0.7 pandas==2.0.3 joblib==1.3.2 scipy==1.11.4
```

Then restart your Flask server:
```bash
python app.py
```

### Option 2: Use Basic Version (Without Enhanced Features)

The app has been updated to work without the new features if dependencies aren't installed. Just restart the server:

```bash
cd resume/backend
python app.py
```

The basic features will work, but authentication, history tracking, and interview prep will be disabled until you install the dependencies.

## Verify Fix

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Check the console output:
   - ✅ If you see: "Enhanced features (auth, history, interview) loaded successfully"
     → All features are enabled!
   
   - ⚠️ If you see: "Enhanced features not available. Install dependencies..."
     → Basic features work, but enhanced features are disabled

3. Test the API:
   ```bash
   curl http://localhost:5000/companies
   ```
   
   Should return JSON like:
   ```json
   {
     "status": "success",
     "companies": ["Google", "Amazon", ...]
   }
   ```

## What Each Feature Requires

### Core Features (Already Working)
- Resume upload and analysis
- Company matching
- ML eligibility scoring
- ATS analysis
- Resume optimization
- Export features

### Enhanced Features (Require New Dependencies)
- ✨ User authentication (requires: PyJWT, bcrypt)
- ✨ Resume history tracking (requires: pandas, joblib)
- ✨ Interview preparation (requires: scipy)
- ✨ Mobile app support

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'jwt'"
**Solution:** Install PyJWT
```bash
pip install PyJWT==2.8.0
```

### Issue: "ModuleNotFoundError: No module named 'bcrypt'"
**Solution:** Install bcrypt
```bash
pip install bcrypt==4.0.1
```

### Issue: Server still crashes
**Solution:** Check Python version (requires 3.8+)
```bash
python --version
```

### Issue: Permission errors on Windows
**Solution:** Run as administrator or use:
```bash
pip install --user PyJWT bcrypt cryptography
```

## Next Steps

After installing dependencies:

1. **Test Authentication:**
   ```bash
   curl -X POST http://localhost:5000/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","first_name":"Test","last_name":"User"}'
   ```

2. **Test History:**
   ```bash
   curl http://localhost:5000/history \
     -H "Authorization: Bearer YOUR_TOKEN"
   ```

3. **Test Interview Prep:**
   ```bash
   curl -X POST http://localhost:5000/interview/start-session \
     -H "Authorization: Bearer YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"company_name":"Google","job_role":"Software Engineer","session_type":"mixed"}'
   ```

## Support

If you continue to have issues:
1. Check the Flask console for detailed error messages
2. Verify all dependencies are installed: `pip list`
3. Try creating a fresh virtual environment
4. Check the ENHANCED_FEATURES_GUIDE.md for detailed setup instructions