@echo off
echo ========================================
echo Real-Time Job Update
echo ========================================
echo.
echo Fetching latest jobs from APIs...
echo.

python job_scraper\real_job_api_scraper.py

echo.
echo ========================================
echo Update Complete!
echo ========================================
echo.
pause