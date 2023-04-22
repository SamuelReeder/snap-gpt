@echo off
python src/check_requirements.py requirements.txt
if errorlevel 1 (
    echo Installing missing packages...
    pip install -r requirements.txt
)
python src/main.py
pause
