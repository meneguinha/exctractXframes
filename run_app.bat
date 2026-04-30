@echo off
echo ===================================================
echo Starting Video Frame Extractor (Streamlit App)
echo ===================================================

:: Ensure the script runs in the directory where the batch file is located
cd /d "%~dp0"

echo Installing/Checking requirements...
pip install -r requirements.txt

echo.
echo Launching the application...
python -m streamlit run app.py

pause
