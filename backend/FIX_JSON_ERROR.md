# 🔧 Fix: "Unexpected token '<', "<!doctype "... is not valid JSON"

## What Happened?

The Flask backend is crashing because new enhanced features were added that require additional Python packages. When the backend crashes, it returns an HTML error page instead of JSON, causing the frontend to show this error.

## Quick Fix (2 Steps)

### Step 1: Install Missing Dependencies

Open a terminal in the `resume/backend` folder and run:

**Windows:**
```bash
install_enhanced_features.bat
```

**Linux/Mac:**
```bash
chmod +x install_enhanced_features.sh
./install_enhanced_features.sh
```

**Or install manually:**
```bash
pip install PyJWT==2.8.0 bcrypt==4.0.1 cryptography==41.0.7
```

### Step 2: Restart the Server

```bash
python app.py
```

You should see:
```
✓ Enhanced features (auth, history, interview) loaded successfully
```

## Verify It's Fixed

1. Open your browser to the frontend
2. The "Error loading companies" should be gone
3. You should see the company list load successfully

## Alternative: Run Without Enhanced Features

If you don't want to install the new dependencies right now, the app will still work with basic features:

1. Just restart the server: `python app.py`
2. You'll see a warning: "Enhanced features not available"
3. Basic features (resume analysis, company matching) will work
4. New features (authentication, history, interview prep) will be disabled

## Check What's Installed

Run this to see which features are available:

```bash
python check_dependencies.py
```

## What Are the New Features?

The enhanced features that require these dependencies:

1. **User Authentication** (requires PyJWT, bcrypt)
   - User registration and login
   - Secure password storage
   - JWT token authentication

2. **Resume History Tracking** (requires pandas)
   - Track all your resume uploads
   - View analysis trends over time
   - Personal analytics dashboard

3. **Interview Preparation** (requires scipy)
   - AI-generated interview questions
   - Practice sessions with feedback
   - Progress tracking

4. **Mobile App Support**
   - React Native mobile app
   - Cross-platform (iOS/Android)

## Still Having Issues?

1. **Check Python version:**
   ```bash
   python --version
   ```
   (Requires Python 3.8 or higher)

2. **Check if Flask is installed:**
   ```bash
   pip list | grep -i flask
   ```

3. **Reinstall all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Check the console for errors:**
   Look at the terminal where you ran `python app.py` for detailed error messages

## Need Help?

See the detailed guides:
- `QUICK_FIX_GUIDE.md` - Detailed troubleshooting
- `ENHANCED_FEATURES_GUIDE.md` - Complete setup guide
- `QUICK_SETUP_GUIDE.md` - Original setup instructions