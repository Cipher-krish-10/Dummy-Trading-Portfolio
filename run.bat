@echo off
echo Setting up virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Running database fix script...
python fix_database.py

echo Starting application...
python app.py

pause 