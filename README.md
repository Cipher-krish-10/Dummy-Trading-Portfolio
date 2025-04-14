Trading Portfolio Management App

A sleek, modern web application for tracking and managing investment portfolios, stocks, and dividends.

## Features

- Modern, responsive UI
- Portfolio Dashboard
- Stock Discovery and Research
- Transaction Tracking
- Smart Watchlists
- User Authentication (simplified without password hashing for demo purposes)

## Local Deployment Instructions

### Prerequisites

- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### Step 1: Set up the database

1. Start your MySQL server
2. Log in to MySQL and run the DB setup script:
```
mysql -u root -p < db_setup.sql
```

### Step 2: Install dependencies

```
pip install -r requirements.txt
```

### Step 3: Configure the application

If needed, modify the database connection settings in `app.py`:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'flask_login'
```

### Step 4: Run the application

```
python app.py
```

The application will be available at http://localhost:5000

### Test User Credentials

- Username: testuser
- Password: password123

Note: For demonstration purposes, passwords are stored in plain text. This is not recommended for production applications.

## Project Structure

- `app.py` - Main application file
- `static/` - CSS, JavaScript, and other static files
- `templates/` - HTML templates
- `requirements.txt` - Python dependencies
- `db_setup.sql` - Database schema and initial data 
