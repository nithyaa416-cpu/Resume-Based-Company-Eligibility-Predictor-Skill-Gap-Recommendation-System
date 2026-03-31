#!/bin/bash

echo "========================================"
echo "Installing Enhanced Features Dependencies"
echo "========================================"
echo ""

echo "Installing authentication dependencies..."
pip install PyJWT==2.8.0
pip install bcrypt==4.0.1
pip install cryptography==41.0.7

echo ""
echo "Installing additional ML dependencies..."
pip install pandas==2.0.3
pip install joblib==1.3.2
pip install scipy==1.11.4

echo ""
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "You can now use:"
echo "- User Authentication"
echo "- Resume History Tracking"
echo "- Interview Preparation Features"
echo ""
echo "Restart your Flask server to enable these features."
echo ""