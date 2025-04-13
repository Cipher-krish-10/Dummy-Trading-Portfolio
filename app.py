from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime
import yfinance as yf
import pandas as pd
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Add a form for admin login
class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Admin Login')

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'krishuppal10'
app.config['MYSQL_DB'] = 'dummy_portfolio'

mysql = MySQL(app)


def populate_stocks_from_yahoo():
    
    stock_tickers = [
        
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'JPM', 'NFLX', 'DIS',
        'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'BAC', 'INTC', 'VZ', 'ADBE',
        'PYPL', 'CMCSA', 'PFE', 'T', 'CRM', 'KO', 'CSCO', 'ABT', 'PEP', 'MRK',
        'XOM', 'CVX', 'ABBV', 'WFC', 'COST', 'MCD', 'TMO', 'ACN', 'AVGO', 'DHR',
        
       
        'ORCL', 'NKE', 'LLY', 'QCOM', 'UNH', 'AMD', 'TXN', 'NEE', 'RTX', 'HON',
        'LIN', 'UNP', 'IBM', 'AMGN', 'PM', 'SBUX', 'MMM', 'CVS', 'GS', 'BMY',
        'LOW', 'CAT', 'GE', 'AXP', 'MDLZ', 'GILD', 'BKNG', 'CHTR', 'TJX', 'ITW',
        'ANTM', 'ADP', 'TGT', 'ISRG', 'LMT', 'BA', 'SPGI', 'ZTS', 'PLD', 'NOC',
        'MO', 'DE', 'ETN', 'MS', 'LRCX', 'MU', 'AMAT', 'REGN', 'CME', 'DUK',
        'CL', 'BLK', 'CCI', 'SO', 'CI', 'CB', 'SCHW', 'COP', 'COF', 'D',
        'VRTX', 'EQIX', 'ADI', 'SYK', 'BDX', 'MET', 'ILMN', 'EMR', 'EW', 'HUM',
        'ICE', 'ATVI', 'NSC', 'A', 'PSA', 'IDXX', 'HCA', 'KLAC', 'BIIB', 'WDAY',
        'MNST', 'ROP', 'SNPS', 'TEL', 'CDNS', 'WM', 'ADSK', 'APD', 'AIG', 'ANSS',
        'PNC', 'EL', 'ORLY', 'ECL', 'FISV', 'DG', 'DXCM', 'TROW', 'ROST', 'CMG',
        'CSX', 'FDX', 'CTSH', 'FAST', 'USB', 'AVB', 'AMT', 'EQR', 'MCO', 'AAP',
        'SBAC', 'AEP', 'GPN', 'MAR', 'GD', 'F', 'DFS', 'STZ', 'PSX', 'SRE',
        'AZO', 'ALL', 'XEL', 'EA', 'APH', 'NDAQ', 'PRU', 'CMI', 'INFO', 'WMB',
        'CTAS', 'TFC', 'HSY', 'AFL', 'MSI', 'BBY', 'AWK', 'PCAR', 'MSCI', 'EOG',
        'PAYX', 'TRV', 'ADM', 'JCI', 'XYL', 'CPRT', 'MCHP', 'ROK', 'DLTR', 'DOW',
        'PPG', 'DD', 'AMP', 'LHX', 'VMC', 'MTD', 'KMB', 'FIS', 'VRSK', 'KEYS',
        'ALGN', 'MKC', 'CARR', 'GLW', 'NXPI', 'WELL', 'HPQ', 'KR', 'CTVA', 'EXC',
        'WY', 'YUM', 'FCX', 'OKE', 'SYY', 'AJG', 'OTIS', 'DTE', 'SPG', 'ES',
        'FRC', 'DOV', 'IQV', 'HLT', 'SWK', 'PH', 'PAYC', 'ETSY', 'ZBRA', 'IT',
        'STT', 'DPZ', 'TWTR', 'CNP', 'RMD', 'BAX', 'DAL', 'ALXN', 'MLM', 'EXPD',
        'URI', 'PXD', 'GNRC', 'GM', 'LVS', 'MKTX', 'GWW', 'ULTA', 'WST', 'FTNT',
        'TSCO', 'PPL', 'XRAY', 'ENPH', 'BIO', 'CHD', 'BLL', 'CLX', 'ESS', 'KMI',
        'CERN', 'SWKS', 'INCY', 'LUV', 'NTRS', 'RCL', 'HIG', 'WAT', 'FTV', 'DGX',
        'ABC', 'VFC', 'IFF', 'HOLX', 'IPG', 'AES', 'NWS', 'LNC', 'GRMN', 'NWL',
        'UDR', 'WDC', 'GPS', 'KIM', 'AIZ', 'BWA', 'MHK', 'ALB', 'LKQ', 'RJF',
        'ABMD', 'AKAM', 'SIVB', 'WAB', 'COO', 'AMCR', 'DISCA', 'JBHT', 'DVN', 'CCL',
        'MRO', 'CF', 'DISCK', 'DVA', 'NCLH', 'WYNN', 'MGM', 'CZR', 'APA', 'HAS',
        'RE', 'HST', 'CFG', 'DXC', 'VNO', 'PVH', 'LB', 'HSIC', 'REG', 'MOS',
        'ALLE', 'WHR', 'HII', 'OXY', 'PEAK', 'SNA', 'PHM', 'ROL', 'RHI', 'FMC',
        'HAL', 'KEY', 'FFIV', 'NLOK', 'HRL', 'LNT', 'RF', 'GPC', 'HES', 'TTWO',
        'NRG', 'JNPR', 'TDY', 'PKI', 'IRM', 'CPB', 'IP', 'TDG', 'HWM', 'WRB',
        'CTLT', 'TER', 'SJM', 'CMA', 'PBCT', 'PFG', 'EMN', 'CHRW', 'KSU', 'SEE',
        'L', 'CINF', 'AAL', 'FBHS', 'FOXA', 'TPR', 'FOX', 'HOG', 'LDOS', 'BKR',
        'PRGO', 'BEN', 'LUMN', 'QRVO', 'LYV', 'DISH', 'CBOE', 'VLO', 'AVY', 'J',
        'ANET', 'EVRG', 'NVR', 'FANG', 'KMX', 'UAL', 'EXPE', 'FLT', 'UHS', 'CE',
        'AOS', 'PWR', 'OMC', 'CNC', 'NI', 'MAS', 'ZION', 'TECH', 'KSS', 'NLSN',
        'TRMB', 'WBA', 'RSG', 'DHI', 'PNR', 'IPGP', 'POOL', 'EFX', 'CDAY', 'ODFL',
        'BR', 'VRSN', 'FITB', 'INTU', 'NOV', 'GIS', 'VIAC', 'APTV', 'MPC', 'NUE',
        'SLB', 'ATO', 'CBRE', 'NTAP', 'HP', 'JKHY', 'NBIX', 'MTCH', 'JNPR', 'HBAN'
    ]
    
    success_count = 0
    error_count = 0
    
    
    for ticker in stock_tickers:
        try:
           
            stock = yf.Ticker(ticker)
            info = stock.info
            
            company_name = info.get("longName", ticker)
            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            market_sector = info.get("sector", "Unknown")
            
            
            cursor = mysql.connection.cursor()
            
            
            cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker,))
            existing = cursor.fetchone()
            
            if not existing:
                
            
                sql = """
                    INSERT INTO STOCK (company_name, ticker_symbol, current_price, market_sector)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (company_name, ticker, current_price, market_sector))
                success_count += 1
            else:
               
                sql = """
                    UPDATE STOCK 
                    SET company_name = %s, current_price = %s, market_sector = %s
                    WHERE ticker_symbol = %s
                """
                cursor.execute(sql, (company_name, current_price, market_sector, ticker))
            
            mysql.connection.commit()
            cursor.close()
            
        except Exception as e:
            error_count += 1
            print(f"Error adding {ticker}: {str(e)}")
            mysql.connection.rollback()
    
    return success_count, error_count


def verify_dividends_table():
    """Explicitly check and create the dividends table"""
    try:
        cursor = mysql.connection.cursor()
        print("\n=== VERIFYING DIVIDENDS TABLE ===")
        
        
        cursor.execute("SHOW TABLES LIKE 'dividends'")
        table_exists = cursor.fetchone() is not None
        print(f"Dividends table exists: {table_exists}")
        
        if not table_exists:
            print("Creating dividends table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dividends (
                    dividend_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ticker_symbol VARCHAR(20) NOT NULL,
                    payment_date DATE NOT NULL,
                    amount_per_share DECIMAL(10, 4) NOT NULL,
                    shares_owned INT NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    is_received BOOLEAN DEFAULT FALSE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
                )
            ''')
            mysql.connection.commit()
            print("Dividends table created successfully!")
        
        
        cursor.execute("DESCRIBE dividends")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        print(f"Dividends table columns: {column_names}")
        
        
        required_columns = ['dividend_id', 'user_id', 'ticker_symbol', 'payment_date', 
                           'amount_per_share', 'shares_owned', 'total_amount', 'is_received']
        
        missing_columns = [col for col in required_columns if col not in column_names]
        if missing_columns:
            print(f"WARNING: Missing columns in dividends table: {missing_columns}")
           
        else:
            print("All required columns exist in the dividends table!")
        
        print("=== DIVIDENDS TABLE VERIFICATION COMPLETE ===\n")
        cursor.close()
        return True
    except Exception as e:
        print(f"ERROR: Failed to verify dividends table: {str(e)}")
        return False

# Add this function to verify the transactions table
def verify_transactions_table():
    """
    Verify that the transactions table exists and has all necessary columns.
    If not, create or alter it to add the required columns.
    """
    try:
        print("Verifying transactions table structure...")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if transactions table exists
        cursor.execute("SHOW TABLES LIKE 'transactions'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("Transactions table doesn't exist, creating it...")
            cursor.execute('''
                CREATE TABLE transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ticker_symbol VARCHAR(20) NOT NULL,
                    transaction_type ENUM('BUY', 'SELL') NOT NULL,
                    quantity INT NOT NULL,
                    price DECIMAL(10, 2),
                    broker_id INT,
                    brokerage_fee DECIMAL(10, 2) DEFAULT 0,
                    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
                )
            ''')
            mysql.connection.commit()
        
        # Check columns
        cursor.execute("DESCRIBE transactions")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        # Add broker_id if it doesn't exist
        if 'broker_id' not in column_names:
            print("Adding broker_id column to transactions table...")
            try:
                cursor.execute('''
                    ALTER TABLE transactions 
                    ADD COLUMN broker_id INT
                ''')
                mysql.connection.commit()
                print("Successfully added broker_id column")
            except Exception as e:
                print(f"Error adding broker_id column: {str(e)}")
        
        # Add brokerage_fee if it doesn't exist
        if 'brokerage_fee' not in column_names:
            print("Adding brokerage_fee column to transactions table...")
            try:
                cursor.execute("ALTER TABLE transactions ADD COLUMN brokerage_fee DECIMAL(10, 2) DEFAULT 0")
                mysql.connection.commit()
                print("Successfully added brokerage_fee column")
            except Exception as e:
                print(f"Failed to add brokerage_fee column: {str(e)}")
        
        cursor.close()
        print("Transactions table verification complete")
    except Exception as e:
        print(f"Error verifying transactions table: {str(e)}")

# Update the setup_database function to explicitly verify dividends
def setup_database():
    try:
        cursor = mysql.connection.cursor()
        
        # Check if user table exists, if not create it
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL
            )
        ''')
        
        # Check if STOCK table exists, if not create it
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS STOCK (
                stock_id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(100) NOT NULL,
                ticker_symbol VARCHAR(20) UNIQUE NOT NULL,
                current_price DECIMAL(10, 2),
                market_sector VARCHAR(50),
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        ''')
        
        # Create portfolio table for users to save their stocks
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS portfolio (
                portfolio_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                ticker_symbol VARCHAR(20) NOT NULL,
                quantity INT DEFAULT 1,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                UNIQUE (user_id, ticker_symbol)
            )
        ''')
        
        # Create broker table for storing broker information
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS broker (
                broker_id INT AUTO_INCREMENT PRIMARY KEY,
                broker_name VARCHAR(100) NOT NULL,
                description TEXT,
                website VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create brokerage table for fee structures
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS brokerage (
                brokerage_id INT AUTO_INCREMENT PRIMARY KEY,
                broker_id INT NOT NULL,
                min_amount DECIMAL(10, 2) DEFAULT 0,
                max_amount DECIMAL(10, 2) DEFAULT 999999999.99,
                brokerage_percentage DECIMAL(5, 2) NOT NULL,
                flat_fee DECIMAL(8, 2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (broker_id) REFERENCES broker(broker_id) ON DELETE CASCADE
            )
        ''')
        
        # Create transactions table to track portfolio changes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                ticker_symbol VARCHAR(20) NOT NULL,
                transaction_type ENUM('BUY', 'SELL') NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(10, 2),
                broker_id INT,
                brokerage_fee DECIMAL(10, 2) DEFAULT 0,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                FOREIGN KEY (broker_id) REFERENCES broker(broker_id) ON DELETE SET NULL
            )
        ''')
        
        # Create watchlist table for users to track stocks they're interested in
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                ticker_symbol VARCHAR(20) NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                UNIQUE (user_id, ticker_symbol)
            )
        ''')
        
        # Create dividends table to track dividend payments
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dividends (
                dividend_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                ticker_symbol VARCHAR(20) NOT NULL,
                payment_date DATE NOT NULL,
                amount_per_share DECIMAL(10, 4) NOT NULL,
                shares_owned INT NOT NULL,
                total_amount DECIMAL(10, 2) NOT NULL,
                is_received BOOLEAN DEFAULT FALSE,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
            )
        ''')
        
        # Insert some default brokers if they don't exist
        cursor.execute("SELECT COUNT(*) as count FROM broker")
        broker_count = cursor.fetchone()[0]
        
        if broker_count == 0:
            cursor.execute('''
                INSERT INTO broker (broker_name, description, website) VALUES
                ('Zerodha', 'Indian discount broker with flat fee structure', 'https://zerodha.com'),
                ('Interactive Brokers', 'Global broker with tiered pricing', 'https://www.interactivebrokers.com'),
                ('Charles Schwab', 'US-based broker with zero commission', 'https://www.schwab.com'),
                ('Robinhood', 'Commission-free stock trading app', 'https://robinhood.com'),
                ('Fidelity', 'Full-service broker with research tools', 'https://www.fidelity.com')
            ''')
            
            # Insert brokerage fee structures
            cursor.execute('''
                INSERT INTO brokerage (broker_id, min_amount, max_amount, brokerage_percentage, flat_fee) VALUES
                (1, 0, 999999999.99, 0.03, 20),  -- Zerodha
                (2, 0, 100000, 0.10, 0),        -- Interactive Brokers tier 1
                (2, 100000, 1000000, 0.08, 0),  -- Interactive Brokers tier 2
                (2, 1000000, 999999999.99, 0.05, 0),  -- Interactive Brokers tier 3
                (3, 0, 999999999.99, 0, 0),     -- Charles Schwab (zero commission)
                (4, 0, 999999999.99, 0, 0),     -- Robinhood (zero commission)
                (5, 0, 999999999.99, 0, 4.95)   -- Fidelity
        ''')
        
        mysql.connection.commit()
        cursor.close()
        print("Database setup completed successfully")
    except Exception as e:
        print(f"Database setup error: {str(e)}")

@app.template_filter('timestamp_to_date')
def timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')

# Main route redirects to login
@app.route('/')
def landing():
    # If user is already logged in, redirect to dashboard
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    # Otherwise, show login page
    return redirect(url_for('login'))

# Old route to home redirects to dashboard
@app.route('/home')
def home():
    if 'loggedin' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Show landing page content with login form
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
        account = cursor.fetchone()
        
        if account and account['password_hash'] == password:
            # Print debugging info
            print(f"Login successful for user: {username}")
            print(f"User ID: {account['user_id']}")
            
            session['loggedin'] = True
            session['user_id'] = account['user_id']
            session['username'] = account['username']
            
            # Print session info
            print(f"Session data: {session}")
            
            return redirect(url_for('dashboard'))
        else:
            form.username.errors.append('Incorrect username or password')
    
    # Pass investment platform marketing content to login page
    return render_template('login.html', form=form, show_marketing=True)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO user (username, email, password_hash) VALUES (%s, %s, %s)",
                           (username, email, password))
            mysql.connection.commit()
            cursor.close()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            mysql.connection.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
    return render_template('register.html')

# Dashboard is now the main home page after login
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM STOCK ORDER BY company_name LIMIT 20")
        stocks = cursor.fetchall()
        cursor.close()
        
      
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT COUNT(*) as count FROM STOCK")
        stock_count = cursor.fetchone()['count']
        cursor.close()
        
        popular_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA']
        return render_template('dashboard.html',
                               username=session['username'],
                               popular_stocks=popular_stocks,
                               stocks=stocks,
                               stock_count=stock_count)
    return redirect(url_for('login'))

@app.route('/stock_data', methods=['GET'])
def stock_data():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker_symbol = request.args.get('symbol', default='AAPL').upper()
    
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info
        hist = stock.history(period='1y')

        # Insert or update stock information in the database
        try:
            cursor = mysql.connection.cursor()
            
            # Check if the stock already exists
            cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker_symbol,))
            existing = cursor.fetchone()

            company_name = info.get("longName", ticker_symbol)
            current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
            market_sector = info.get("sector", "Unknown")

            if not existing:
                # Insert new stock record
                sql = """
                    INSERT INTO STOCK (company_name, ticker_symbol, current_price, market_sector)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (company_name, ticker_symbol, current_price, market_sector))
            else:
                # Update existing stock record
                sql = """
                    UPDATE STOCK 
                    SET company_name = %s, current_price = %s, market_sector = %s
                    WHERE ticker_symbol = %s
                """
                cursor.execute(sql, (company_name, current_price, market_sector, ticker_symbol))
            
            mysql.connection.commit()
            cursor.close()
        except Exception as e:
            mysql.connection.rollback()
            print(f"Database error: {str(e)}")
            # Continue even if database operation fails

        # Process historical data for chart
        hist_data = {
            'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            'prices': hist['Close'].tolist(),
            'volumes': hist['Volume'].tolist()
        }

        news = stock.news

        return render_template(
            'stock_data.html',
            ticker=ticker_symbol,
            info=info,
            hist_data=hist_data,
            news=news,
            username=session.get('username', '')
        )
    except Exception as e:
        flash(f'Error fetching stock data: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

@app.route('/search_stock', methods=['POST'])
def search_stock():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = request.form.get('ticker', '').upper()
    if ticker:
        return redirect(url_for('stock_data', symbol=ticker))
    else:
        flash('Please enter a valid ticker symbol', 'error')
        return redirect(url_for('dashboard'))

@app.route('/compare_stocks', methods=['GET'])
def compare_stocks():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    tickers = request.args.get('symbols', 'AAPL,MSFT,GOOGL').upper().split(',')
    
    try:
        data = yf.download(tickers, period='1y')['Close']
        chart_data = {
            'dates': data.index.strftime('%Y-%m-%d').tolist(),
            'stocks': {}
        }

        for ticker in tickers:
            if len(tickers) == 1:
                chart_data['stocks'][ticker] = data.tolist() if not data.empty else []
            else:
                chart_data['stocks'][ticker] = data[ticker].tolist() if ticker in data.columns else []

        return render_template(
            'compare_stocks.html',
            tickers=tickers,
            chart_data=chart_data,
            username=session.get('username', '')
        )
    except Exception as e:
        flash(f'Error comparing stocks: {str(e)}', 'error')
        return redirect(url_for('dashboard'))

# Add route to populate stocks
@app.route('/populate_stocks')
def populate_stocks_route():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    try:
        success_count, error_count = populate_stocks_from_yahoo()
        flash(f'Successfully added/updated {success_count} stocks. Failed: {error_count}', 'success')
    except Exception as e:
        flash(f'Error populating stocks: {str(e)}', 'error')
    
    return redirect(url_for('dashboard'))

@app.route('/search_database_stocks', methods=['GET', 'POST'])
def search_database_stocks():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
        
        if search_term:
            # Search in both ticker symbol and company name using LIKE
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("""
                SELECT * FROM STOCK 
                WHERE ticker_symbol LIKE %s OR company_name LIKE %s
                ORDER BY ticker_symbol
            """, (f'%{search_term}%', f'%{search_term}%'))
            search_results = cursor.fetchall()
            cursor.close()
            
            # Get count of all stocks for reference
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT COUNT(*) as count FROM STOCK")
            stock_count = cursor.fetchone()['count']
            cursor.close()
            
            return render_template('search_results.html',
                                  search_term=search_term,
                                  stocks=search_results,
                                  result_count=len(search_results),
                                  stock_count=stock_count,
                                  username=session['username'])
        
    # If not POST or no search term, redirect to dashboard
    return redirect(url_for('dashboard'))

# Portfolio Management Routes

@app.route('/view_portfolio')
def view_portfolio():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    print(f"Viewing portfolio for user_id: {user_id}")
    
    # Get the user's portfolio stocks
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Debug - print all portfolios
    cursor.execute("SELECT * FROM portfolio")
    all_portfolios = cursor.fetchall()
    print(f"All portfolios in database: {all_portfolios}")
    
    # Get portfolio structure to determine which quantity field to use
    cursor.execute("DESCRIBE portfolio")
    columns = cursor.fetchall()
    column_names = [col['Field'] for col in columns]
    print(f"Portfolio columns: {column_names}")
    
    quantity_field = "quantity" if "quantity" in column_names else "quantity_held"
    
    # Get user's portfolio with stock details
    cursor.execute(f"""
        SELECT p.*, s.company_name, s.current_price, s.market_sector
        FROM portfolio p
        LEFT JOIN STOCK s ON p.ticker_symbol = s.ticker_symbol
        WHERE p.user_id = %s
    """, (user_id,))
    
    portfolio_stocks = cursor.fetchall()
    print(f"Portfolio stocks for user {user_id}: {portfolio_stocks}")
    
    # Get all brokers for dropdown
    cursor.execute("SELECT * FROM broker ORDER BY broker_name")
    brokers = cursor.fetchall()
    
    # Calculate total value
    total_value = 0
    for stock in portfolio_stocks:
        if stock['current_price'] and stock[quantity_field]:
            total_value += stock['current_price'] * stock[quantity_field]
    
    cursor.close()
    
    return render_template('portfolio.html', 
                         username=session['username'],
                         portfolio_stocks=portfolio_stocks, 
                         portfolio_count=len(portfolio_stocks),
                         total_value=total_value,
                         brokers=brokers)

@app.route('/add_to_portfolio/<ticker>')
def add_to_portfolio(ticker):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = ticker.upper()
    user_id = session['user_id']
    
    # Get the broker_id from the request
    broker_id = request.args.get('broker_id')
    if broker_id:
        broker_id = int(broker_id)
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if stock exists in STOCK table
        cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker,))
        stock = cursor.fetchone()
        
        if not stock:
            flash(f"Stock {ticker} not found. Please search for it first.", "error")
            cursor.close()
            return redirect(url_for('dashboard'))
        
        try:
            # First, check if it's already in portfolio
            cursor.execute("""
                SELECT * FROM portfolio
                WHERE user_id = %s AND ticker_symbol = %s
            """, (user_id, ticker))
            
            exists = cursor.fetchone()
            
            if exists:
                flash(f"{ticker} is already in your portfolio! You can update the quantity on your portfolio page.", "warning")
            else:
                # Add to portfolio
                cursor.execute("""
                    INSERT INTO portfolio (user_id, ticker_symbol)
                    VALUES (%s, %s)
                """, (user_id, ticker))
                
                # Calculate transaction amount
                transaction_amount = stock['current_price']  # Default to buying 1 share
                
                # Calculate brokerage fee using our new function
                brokerage_fee = calculate_brokerage_fee(cursor, broker_id, transaction_amount)
                
                # Log the transaction
                try:
                    cursor.execute("""
                        INSERT INTO transactions 
                        (user_id, ticker_symbol, transaction_type, quantity, price, broker_id, brokerage_fee)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (user_id, ticker, 'BUY', 1, stock['current_price'], broker_id, brokerage_fee))
                    
                    mysql.connection.commit()
                    print(f"Transaction logged: BUY {ticker} with brokerage fee ${brokerage_fee}")
                except Exception as e:
                    print(f"Warning: Could not log transaction: {str(e)}")
            
            flash(f"{ticker} added to your portfolio!", "success")
        except Exception as e:
            mysql.connection.rollback()
            print(f"Error adding to portfolio: {str(e)}")
            flash(f"Error adding to portfolio: {str(e)}", "error")
            
        cursor.close()
    except Exception as e:
        print(f"General error: {str(e)}")
        flash(f"Error: {str(e)}", "error")
    
    # Check where the request came from and redirect accordingly
    referrer = request.referrer
    if referrer and 'portfolio' in referrer:
        return redirect(url_for('view_portfolio'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/remove_from_portfolio/<ticker>')
def remove_from_portfolio(ticker):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = ticker.upper()
    user_id = session['user_id']
    
    # Get the broker_id from the request
    broker_id = request.args.get('broker_id')
    if broker_id:
        broker_id = int(broker_id)
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get stock information
        cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker,))
        stock = cursor.fetchone()
        
        if not stock:
            flash(f"Stock {ticker} not found!", "error")
            cursor.close()
            return redirect(url_for('view_portfolio'))
        
        # Get current quantity
        cursor.execute("SELECT quantity FROM portfolio WHERE user_id = %s AND ticker_symbol = %s", (user_id, ticker))
        portfolio_entry = cursor.fetchone()
        
        if not portfolio_entry:
            flash(f"{ticker} is not in your portfolio!", "warning")
            cursor.close()
            return redirect(url_for('view_portfolio'))
        
        quantity = portfolio_entry['quantity']
        
        # Delete from portfolio
        cursor.execute("""
            DELETE FROM portfolio
            WHERE user_id = %s AND ticker_symbol = %s
        """, (user_id, ticker))
        
        # Calculate transaction amount
        transaction_amount = stock['current_price'] * quantity
        
        # Calculate brokerage fee using our new function
        brokerage_fee = calculate_brokerage_fee(cursor, broker_id, transaction_amount)
        
        # Log the transaction
        cursor.execute("""
            INSERT INTO transactions 
            (user_id, ticker_symbol, transaction_type, quantity, price, broker_id, brokerage_fee)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (user_id, ticker, 'SELL', quantity, stock['current_price'], broker_id, brokerage_fee))
        
        mysql.connection.commit()
        cursor.close()
        
        flash(f"{ticker} removed from your portfolio!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error removing from portfolio: {str(e)}", "error")
    
    return redirect(url_for('view_portfolio'))

# Update the brokerage fee calculation function to work with the simplified table
def calculate_brokerage_fee(cursor, broker_id, transaction_amount):
    """
    Calculate brokerage fee based on the broker_id and transaction_amount
    using the percentage from the brokerage table.
    
    Args:
        cursor: Database cursor
        broker_id: ID of the broker
        transaction_amount: Total amount of the transaction
        
    Returns:
        Calculated brokerage fee
    """
    if not broker_id or transaction_amount <= 0:
        return 0.00
    
    try:
        # Get the brokerage percentage directly from the simplified brokerage table
        cursor.execute("""
            SELECT brokerage_percentage 
            FROM brokerage 
            WHERE broker_id = %s
            LIMIT 1
        """, (broker_id,))
        
        result = cursor.fetchone()
        
        if result and 'brokerage_percentage' in result:
            # Calculate fee based on percentage
            percentage = result['brokerage_percentage']
            fee = transaction_amount * (percentage / 100)
            return round(fee, 2)
        else:
            # No brokerage percentage found
            print(f"No brokerage percentage found for broker {broker_id}")
            return 0.00
    except Exception as e:
        print(f"Error calculating brokerage fee: {str(e)}")
        return 0.00

@app.route('/update_portfolio_quantity', methods=['POST'])
def update_portfolio_quantity():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = request.form.get('ticker')
    quantity = int(request.form.get('quantity', 0))
    broker_id = request.form.get('broker_id')
    
    if broker_id:
        broker_id = int(broker_id)  # Convert to integer
    
    if quantity < 0:
        flash("Quantity cannot be negative!", "danger")
        return redirect(url_for('view_portfolio'))
    
    user_id = session['user_id']
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Get stock details
        cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker,))
        stock = cursor.fetchone()
        
        if not stock:
            flash(f"Stock {ticker} not found!", "danger")
            return redirect(url_for('view_portfolio'))
        
        # Get current quantity
        cursor.execute("SELECT quantity FROM portfolio WHERE user_id = %s AND ticker_symbol = %s", (user_id, ticker))
        result = cursor.fetchone()
        current_quantity = result['quantity'] if result else 0
        
        if quantity == 0:
            # Remove from portfolio
            cursor.execute("DELETE FROM portfolio WHERE user_id = %s AND ticker_symbol = %s", (user_id, ticker))
            flash(f"{ticker} removed from your portfolio!", "success")
        else:
            # Insert or update
            if current_quantity == 0:
                cursor.execute("INSERT INTO portfolio (user_id, ticker_symbol, quantity, added_date) VALUES (%s, %s, %s, NOW())", 
                               (user_id, ticker, quantity))
            else:
                cursor.execute("UPDATE portfolio SET quantity = %s WHERE user_id = %s AND ticker_symbol = %s", 
                               (quantity, user_id, ticker))
            
            # Log the transaction - if quantity increased, it's a BUY, otherwise SELL
            if stock and quantity != current_quantity:
                quantity_diff = abs(quantity - current_quantity)
                transaction_type = 'BUY' if quantity > current_quantity else 'SELL'
                
                # Calculate total transaction amount
                total_amount = quantity_diff * stock['current_price']
                
                # Calculate brokerage fee using the new function
                brokerage_fee = calculate_brokerage_fee(cursor, broker_id, total_amount)
                
                cursor.execute("""
                    INSERT INTO transactions 
                    (user_id, ticker_symbol, transaction_type, quantity, price, broker_id, brokerage_fee)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (user_id, ticker, transaction_type, quantity_diff, stock['current_price'], broker_id, brokerage_fee))
        
        mysql.connection.commit()
        cursor.close()
        
        flash(f"{ticker} quantity updated to {quantity}!", "success")
        return redirect(url_for('view_portfolio'))
    except Exception as e:
        cursor.close()
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('view_portfolio'))

@app.route('/transactions')
def view_transactions():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Log which tables are being accessed
        print("DEBUG: Checking broker and brokerage tables...")
        
        # Check if broker table exists and has data
        cursor.execute("SELECT COUNT(*) as count FROM broker")
        broker_count = cursor.fetchone()['count']
        print(f"DEBUG: Found {broker_count} brokers in broker table")
        
        # Check if brokerage table exists and has data
        cursor.execute("SHOW TABLES LIKE 'brokerage'")
        brokerage_exists = cursor.fetchone() is not None
        print(f"DEBUG: Brokerage table exists: {brokerage_exists}")
        
        if brokerage_exists:
            cursor.execute("SELECT COUNT(*) as count FROM brokerage")
            brokerage_count = cursor.fetchone()['count']
            print(f"DEBUG: Found {brokerage_count} entries in brokerage table")
        
        # First, get transactions with basic info
        basic_query = '''
            SELECT t.*, s.company_name
            FROM transactions t
            LEFT JOIN STOCK s ON t.ticker_symbol = s.ticker_symbol
            WHERE t.user_id = %s
            ORDER BY t.transaction_date DESC
        '''
        
        cursor.execute(basic_query, (user_id,))
        transactions = cursor.fetchall()
        print(f"DEBUG: Found {len(transactions)} transactions")
        
        # Then, for each transaction add broker info
        for t in transactions:
            if t['broker_id']:
                cursor.execute('''
                    SELECT broker_name FROM broker WHERE broker_id = %s
                ''', (t['broker_id'],))
                broker = cursor.fetchone()
                if broker:
                    t['broker_name'] = broker['broker_name']
                    print(f"DEBUG: Added broker name {broker['broker_name']} to transaction {t['transaction_id']}")
                else:
                    t['broker_name'] = 'Unknown'
                
                # Get brokerage percentage if available
                if brokerage_exists:
                    cursor.execute('''
                        SELECT brokerage_percentage FROM brokerage WHERE broker_id = %s
                    ''', (t['broker_id'],))
                    brokerage = cursor.fetchone()
                    if brokerage:
                        t['brokerage_percentage'] = brokerage['brokerage_percentage']
                    else:
                        t['brokerage_percentage'] = 0
        
        # Include brokerage fees in summary query
        cursor.execute('''
            SELECT 
                SUM(CASE WHEN transaction_type = 'BUY' THEN quantity * price ELSE 0 END) as total_buys,
                SUM(CASE WHEN transaction_type = 'SELL' THEN quantity * price ELSE 0 END) as total_sells,
                SUM(brokerage_fee) as total_brokerage_fees,
                COUNT(*) as total_transactions
            FROM transactions
            WHERE user_id = %s
        ''', (user_id,))
        
        summary = cursor.fetchone()
        
        # Get all brokers for the dropdown
        cursor.execute("SELECT * FROM broker ORDER BY broker_name")
        brokers = cursor.fetchall()
        
        # Get brokerage percentages for display
        broker_fees = []
        if brokerage_exists:
            cursor.execute('''
                SELECT b.broker_id, b.broker_name, br.brokerage_percentage 
                FROM broker b
                LEFT JOIN brokerage br ON b.broker_id = br.broker_id
                ORDER BY b.broker_name
            ''')
            broker_fees = cursor.fetchall()
        
        cursor.close()
        
        return render_template('transaction_history.html', 
                               username=session['username'],
                               transactions=transactions,
                               summary=summary,
                               brokers=brokers,
                               broker_fees=broker_fees,
                               has_broker_id=True,
                               has_brokerage_fee=True)
    except Exception as e:
        flash(f"Error retrieving transaction history: {str(e)}", "error")
        print(f"TRANSACTION ERROR: {str(e)}")
        return redirect(url_for('dashboard'))

# Watchlist Routes
@app.route('/watchlist')
def view_watchlist():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check watchlist table structure
        cursor.execute("DESCRIBE watchlist")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        print(f"Watchlist columns: {column_names}")
        
        # Determine if ticker_symbol exists or if it might be using another name
        ticker_field = "ticker_symbol"
        if "ticker_symbol" not in column_names and "ticker" in column_names:
            ticker_field = "ticker"
        elif "ticker_symbol" not in column_names and "symbol" in column_names:
            ticker_field = "symbol"
        
        print(f"Using field {ticker_field} for watchlist stock symbol")
        
        # Get all watchlist stocks for this user with their details using the appropriate field name
        query = f'''
            SELECT w.*, s.company_name, s.current_price, s.market_sector
            FROM watchlist w
            JOIN STOCK s ON w.{ticker_field} = s.ticker_symbol
            WHERE w.user_id = %s
            ORDER BY w.added_date DESC
        '''
        print(f"Executing query: {query}")
        
        cursor.execute(query, (user_id,))
        watchlist_stocks = cursor.fetchall()
        
        # Get count of stocks in watchlist
        watchlist_count = len(watchlist_stocks)
        
        cursor.close()
        
        return render_template('watchlist.html', 
                               username=session['username'],
                               watchlist_stocks=watchlist_stocks,
                               watchlist_count=watchlist_count)
    except Exception as e:
        flash(f"Error retrieving watchlist: {str(e)}", "error")
        # If the watchlist table might not exist, let's try to create it
        try:
            cursor = mysql.connection.cursor()
            print("Attempting to recreate watchlist table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS watchlist (
                    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ticker_symbol VARCHAR(20) NOT NULL,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                    UNIQUE (user_id, ticker_symbol)
                )
            ''')
            mysql.connection.commit()
            cursor.close()
            print("Watchlist table created or confirmed")
            flash("Watchlist table setup complete. Please try again.", "info")
        except Exception as create_error:
            print(f"Error recreating watchlist table: {str(create_error)}")
        
        return redirect(url_for('dashboard'))

@app.route('/add_to_watchlist/<ticker>')
def add_to_watchlist(ticker):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = ticker.upper()
    user_id = session['user_id']
    
    print(f"Adding {ticker} to watchlist for user_id: {user_id}")
    
    try:
        # Check if stock exists in STOCK table
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM STOCK WHERE ticker_symbol = %s", (ticker,))
        stock = cursor.fetchone()
        
        if not stock:
            # If stock doesn't exist in database, fetch it from Yahoo Finance
            try:
                stock_data = yf.Ticker(ticker)
                info = stock_data.info
                
                company_name = info.get("longName", ticker)
                current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
                market_sector = info.get("sector", "Unknown")
                
                # Add stock to database
                cursor.execute("""
                    INSERT INTO STOCK (company_name, ticker_symbol, current_price, market_sector)
                    VALUES (%s, %s, %s, %s)
                """, (company_name, ticker, current_price, market_sector))
                mysql.connection.commit()
            except Exception as e:
                print(f"Error fetching stock data: {str(e)}")
                flash(f"Error fetching stock data: {str(e)}", "error")
                return redirect(url_for('dashboard'))
        
        # Check watchlist table structure
        cursor.execute("DESCRIBE watchlist")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        # Determine if ticker_symbol exists or if it might be using another name
        ticker_field = "ticker_symbol"
        if "ticker_symbol" not in column_names and "ticker" in column_names:
            ticker_field = "ticker"
        elif "ticker_symbol" not in column_names and "symbol" in column_names:
            ticker_field = "symbol"
            
        print(f"Using field {ticker_field} for watchlist stock symbol")
        
        # Add stock to user's watchlist if it doesn't already exist
        query = f"""
            INSERT IGNORE INTO watchlist (user_id, {ticker_field})
            VALUES (%s, %s)
        """
        cursor.execute(query, (user_id, ticker))
        
        mysql.connection.commit()
        cursor.close()
        
        flash(f"{ticker} added to your watchlist!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error adding to watchlist: {str(e)}", "error")
        
        # If there's an error, make sure the watchlist table exists
        try:
            cursor = mysql.connection.cursor()
            print("Attempting to create/fix watchlist table...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS watchlist (
                    watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ticker_symbol VARCHAR(20) NOT NULL,
                    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                    UNIQUE (user_id, ticker_symbol)
                )
            ''')
            mysql.connection.commit()
        except Exception as create_error:
            print(f"Error creating watchlist table: {str(create_error)}")
    
    # Check where the request came from and redirect accordingly
    referrer = request.referrer
    if referrer and 'watchlist' in referrer:
        return redirect(url_for('view_watchlist'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/remove_from_watchlist/<ticker>')
def remove_from_watchlist(ticker):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = ticker.upper()
    user_id = session['user_id']
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check watchlist table structure
        cursor.execute("DESCRIBE watchlist")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        # Determine if ticker_symbol exists or if it might be using another name
        ticker_field = "ticker_symbol"
        if "ticker_symbol" not in column_names and "ticker" in column_names:
            ticker_field = "ticker"
        elif "ticker_symbol" not in column_names and "symbol" in column_names:
            ticker_field = "symbol"
            
        print(f"Using field {ticker_field} for watchlist stock symbol")
        
        # Remove from watchlist using the correct field name
        query = f"""
            DELETE FROM watchlist
            WHERE user_id = %s AND {ticker_field} = %s
        """
        cursor.execute(query, (user_id, ticker))
        
        mysql.connection.commit()
        cursor.close()
        
        flash(f"{ticker} removed from your watchlist!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error removing from watchlist: {str(e)}", "error")
    
    return redirect(url_for('view_watchlist'))

@app.route('/update_watchlist_notes', methods=['POST'])
def update_watchlist_notes():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = request.form.get('ticker', '').upper()
    notes = request.form.get('notes', '')
    user_id = session['user_id']
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check watchlist table structure
        cursor.execute("DESCRIBE watchlist")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        # Determine if ticker_symbol exists or if it might be using another name
        ticker_field = "ticker_symbol"
        if "ticker_symbol" not in column_names and "ticker" in column_names:
            ticker_field = "ticker"
        elif "ticker_symbol" not in column_names and "symbol" in column_names:
            ticker_field = "symbol"
            
        print(f"Using field {ticker_field} for watchlist stock symbol")
        
        # Update notes using the correct field name
        query = f"""
            UPDATE watchlist
            SET notes = %s
            WHERE user_id = %s AND {ticker_field} = %s
        """
        cursor.execute(query, (notes, user_id, ticker))
        
        mysql.connection.commit()
        cursor.close()
        
        flash(f"Notes updated for {ticker}!", "success")
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error updating notes: {str(e)}", "error")
    
    return redirect(url_for('view_watchlist'))

@app.route('/dividend_data/<ticker>')
def dividend_data(ticker):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    ticker = ticker.upper()
    
    try:
        # Get stock data from Yahoo Finance
        stock = yf.Ticker(ticker)
        
        # Get dividend data
        dividends = stock.dividends
        
        # If no dividends, return empty
        if dividends.empty:
            flash(f"No dividend data available for {ticker}", "info")
            return redirect(url_for('stock_data', symbol=ticker))
        
        # Convert to DataFrame with reset index to make date accessible
        dividends_df = dividends.reset_index()
        
        # Format the data for the template
        dividend_data = []
        for _, row in dividends_df.iterrows():
            dividend_data.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'amount': float(row['Dividends'])
            })
        
        # Get company info
        info = stock.info
        company_name = info.get('longName', ticker)
        
        # Calculate annual dividend yield if available
        current_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
        trailing_annual_dividend_rate = info.get('trailingAnnualDividendRate', 0)
        dividend_yield = info.get('dividendYield', 0)
        
        if dividend_yield:
            dividend_yield = dividend_yield * 100  # Convert to percentage
        
        # Calculate total dividends and averages
        total_dividends = sum(div['amount'] for div in dividend_data)
        avg_dividend = total_dividends / len(dividend_data) if dividend_data else 0
        
        # Get the latest dividend date and amount
        latest_dividend = dividend_data[0] if dividend_data else {'date': 'N/A', 'amount': 0}
        
        # Render the template with the data
        return render_template(
            'dividend_data.html',
            ticker=ticker,
            company_name=company_name,
            dividend_data=dividend_data,
            current_price=current_price,
            dividend_yield=dividend_yield,
            trailing_annual_dividend_rate=trailing_annual_dividend_rate,
            total_dividends=total_dividends,
            avg_dividend=avg_dividend,
            latest_dividend=latest_dividend,
            username=session['username']
        )
        
    except Exception as e:
        flash(f"Error retrieving dividend data: {str(e)}", "error")
        return redirect(url_for('dashboard'))

@app.route('/dividend_income')
def dividend_income():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Get the user's portfolio stocks
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get portfolio structure to determine which quantity field to use
        cursor.execute("DESCRIBE portfolio")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        quantity_field = "quantity" if "quantity" in column_names else "quantity_held"
        
        # Get this user's portfolio with appropriate quantity field
        cursor.execute(f'''
            SELECT p.*, s.company_name, s.current_price, s.ticker_symbol,
                   p.{quantity_field} as display_quantity
            FROM portfolio p
            JOIN STOCK s ON p.ticker_symbol = s.ticker_symbol
            WHERE p.user_id = %s
        ''', (user_id,))
        
        portfolio_stocks = cursor.fetchall()
        cursor.close()
        
        
        dividend_data = []
        total_annual_dividend = 0
        portfolio_value = 0
        
        for stock in portfolio_stocks:
            ticker = stock['ticker_symbol']
            quantity = float(stock['display_quantity'])
            current_price = float(stock['current_price'])
            stock_value = current_price * quantity
            portfolio_value += stock_value
            
            
            yf_stock = yf.Ticker(ticker)
            info = yf_stock.info
            
            
            trailing_annual_dividend_rate = info.get('trailingAnnualDividendRate', 0)
            dividend_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
            
            
            annual_dividend_income = trailing_annual_dividend_rate * quantity
            total_annual_dividend += annual_dividend_income
            
            
            dividends = yf_stock.dividends
            recent_dividend = 0
            payment_frequency = 0
            
            if not dividends.empty:
                
                recent_dividend = float(dividends.iloc[-1])
                
                
                if len(dividends) > 1:
                    
                    dates = dividends.index
                    if len(dates) >= 2:
                        
                        date_diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
                        avg_days = sum(date_diffs) / len(date_diffs)
                        
                        
                        if avg_days < 60:  
                            payment_frequency = 12
                        elif avg_days < 100:  
                            payment_frequency = 4
                        elif avg_days < 200:  
                            payment_frequency = 2
                        else:  
                            payment_frequency = 1
            
            dividend_data.append({
                'ticker': ticker,
                'company_name': stock['company_name'],
                'quantity': quantity,
                'stock_value': stock_value,
                'dividend_yield': dividend_yield,
                'annual_dividend_rate': trailing_annual_dividend_rate,
                'annual_income': annual_dividend_income,
                'recent_dividend': recent_dividend,
                'payment_frequency': payment_frequency
            })
        
        
        portfolio_dividend_yield = (total_annual_dividend / portfolio_value * 100) if portfolio_value > 0 else 0
        
        return render_template(
            'dividend_income.html',
            username=session['username'],
            dividend_data=dividend_data,
            total_annual_dividend=total_annual_dividend,
            portfolio_value=portfolio_value,
            portfolio_dividend_yield=portfolio_dividend_yield
        )
        
    except Exception as e:
        flash(f"Error retrieving dividend income: {str(e)}", "error")
        return redirect(url_for('dashboard'))

@app.route('/update_dividend_history')
def update_dividend_history():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    print(f"Updating dividend history for user_id: {user_id}")
    
    try:
        
        verify_dividends_table()
        
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        
        cursor.execute("DESCRIBE portfolio")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        
        quantity_field = "quantity" if "quantity" in column_names else "quantity_held"
        print(f"Using quantity field: {quantity_field}")
        
        
        cursor.execute(f'''
            SELECT p.*, s.company_name, s.current_price, s.ticker_symbol,
                   p.{quantity_field} as display_quantity
            FROM portfolio p
            JOIN STOCK s ON p.ticker_symbol = s.ticker_symbol
            WHERE p.user_id = %s
        ''', (user_id,))
        
        portfolio_stocks = cursor.fetchall()
        print(f"Found {len(portfolio_stocks)} stocks in portfolio")
        
        if not portfolio_stocks:
            flash("No stocks found in your portfolio. Add stocks first.", "warning")
            return redirect(url_for('view_portfolio'))
        
        
        cursor.execute("SHOW TABLES LIKE 'dividends'")
        dividend_table_exists = cursor.fetchone()
        if not dividend_table_exists:
            print("CRITICAL: Dividends table doesn't exist after verification! Creating now...")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS dividends (
                    dividend_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    ticker_symbol VARCHAR(20) NOT NULL,
                    payment_date DATE NOT NULL,
                    amount_per_share DECIMAL(10, 4) NOT NULL,
                    shares_owned INT NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    is_received BOOLEAN DEFAULT FALSE,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
                )
            ''')
            mysql.connection.commit()
            print("Dividends table created successfully - SECOND ATTEMPT")
        
        
        try:
            cursor.execute('''
                SELECT ticker_symbol, MAX(payment_date) as last_payment_date
                FROM dividends
                WHERE user_id = %s
                GROUP BY ticker_symbol
            ''', (user_id,))
            
            dividend_records = {}
            for row in cursor.fetchall():
                dividend_records[row['ticker_symbol']] = row['last_payment_date']
            
            print(f"Found existing dividend records for {len(dividend_records)} stocks")
        except Exception as e:
            print(f"Error querying existing dividend records: {str(e)}")
            
            dividend_records = {}
        
        
        updated_count = 0
        new_records_count = 0
        processed_stocks = []
        failed_stocks = []
        
        
        for stock in portfolio_stocks:
            ticker = stock['ticker_symbol']
            quantity = int(stock['display_quantity'])
            print(f"Processing dividends for {ticker}, quantity: {quantity}")
            
           
            try:
                yf_stock = yf.Ticker(ticker)
                dividends = yf_stock.dividends
                
                if dividends.empty:
                    print(f"No dividend data found for {ticker}")
                    continue
                    
                print(f"Found {len(dividends)} dividend records for {ticker}")
                
                
                dividends_df = dividends.reset_index()
                
                
                last_payment_date = dividend_records.get(ticker)
                if last_payment_date:
                    print(f"Last recorded dividend for {ticker} was on {last_payment_date}")
                
               
                records_added_for_stock = 0
                
                for _, row in dividends_df.iterrows():
                    payment_date = row['Date'].strftime('%Y-%m-%d')
                    
                    
                    if last_payment_date and payment_date <= last_payment_date.strftime('%Y-%m-%d'):
                        continue
                    
                    amount_per_share = float(row['Dividends'])
                    total_amount = amount_per_share * quantity
                    
                    print(f"Adding dividend record: {ticker} on {payment_date}, ${amount_per_share}/share, total: ${total_amount}")
                    
                    try:
                       
                        insert_query = '''
                            INSERT INTO dividends 
                            (user_id, ticker_symbol, payment_date, amount_per_share, shares_owned, total_amount, is_received)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        '''
                        insert_values = (
                            user_id, 
                            ticker, 
                            payment_date, 
                            amount_per_share, 
                            quantity, 
                            total_amount,
                            True  
                        )
                        
                        cursor.execute(insert_query, insert_values)
                        mysql.connection.commit()  
                        
                        new_records_count += 1
                        records_added_for_stock += 1
                        print(f"Inserted record #{new_records_count} successfully")
                    except Exception as insert_error:
                        print(f"ERROR inserting dividend record for {ticker} on {payment_date}: {str(insert_error)}")
                        mysql.connection.rollback()
                
                if records_added_for_stock > 0:
                    updated_count += 1
                    processed_stocks.append(ticker)
                
            except Exception as e:
                print(f"Error getting dividend data for {ticker}: {str(e)}")
                failed_stocks.append(ticker)
                continue
        
        
        print(f"Committing {new_records_count} new dividend records to database")
        mysql.connection.commit()
        
        
        try:
            verify_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            verify_cursor.execute("SELECT COUNT(*) as count FROM dividends WHERE user_id = %s", (user_id,))
            count_result = verify_cursor.fetchone()
            verify_cursor.close()
            print(f"Verification: Found {count_result['count']} total dividend records for user")
        except Exception as verify_error:
            print(f"Error verifying dividend records: {str(verify_error)}")
        
        cursor.close()
        
        if new_records_count > 0:
            flash(f"Successfully added {new_records_count} new dividend records for {updated_count} stocks.", "success")
            if failed_stocks:
                flash(f"Failed to process {len(failed_stocks)} stocks: {', '.join(failed_stocks)}", "warning")
        else:
            if processed_stocks:
                flash(f"No new dividend records found for your stocks.", "info")
            else:
                flash("No dividend data could be processed. Check the console for errors.", "warning")
        
        return redirect(url_for('dividend_income'))
        
    except Exception as e:
        print(f"CRITICAL ERROR in update_dividend_history: {str(e)}")
        flash(f"Error updating dividend history: {str(e)}", "error")
        return redirect(url_for('dashboard'))

@app.route('/dividend_history')
def dividend_history():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        
        cursor.execute('''
            SELECT d.*, s.company_name 
            FROM dividends d
            JOIN STOCK s ON d.ticker_symbol = s.ticker_symbol
            WHERE d.user_id = %s
            ORDER BY d.payment_date DESC
        ''', (user_id,))
        
        dividend_records = cursor.fetchall()
        
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_records,
                SUM(total_amount) as total_received,
                COUNT(DISTINCT ticker_symbol) as unique_stocks,
                MAX(payment_date) as latest_payment,
                MIN(payment_date) as earliest_payment
            FROM dividends
            WHERE user_id = %s
        ''', (user_id,))
        
        summary = cursor.fetchone()
        
       
        cursor.execute('''
            SELECT 
                DATE_FORMAT(payment_date, '%Y-%m') as month,
                SUM(total_amount) as monthly_total
            FROM dividends
            WHERE user_id = %s
            GROUP BY DATE_FORMAT(payment_date, '%Y-%m')
            ORDER BY month
        ''', (user_id,))
        
        monthly_totals = cursor.fetchall()
        
      
        months = []
        totals = []
        
        for month_data in monthly_totals:
            month = month_data['month']
            total = float(month_data['monthly_total'])
            
           
            year, month_num = month.split('-')
            month_name = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][int(month_num) - 1]
            
            months.append(f"{month_name} {year}")
            totals.append(total)
        
        cursor.close()
        
        return render_template(
            'dividend_history.html',
            username=session['username'],
            dividend_records=dividend_records,
            summary=summary,
            months=months,
            totals=totals
        )
        
    except Exception as e:
        flash(f"Error retrieving dividend history: {str(e)}", "error")
        return redirect(url_for('dashboard'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        
        if username == "admin" and password == "adminpass":
            session['admin_loggedin'] = True
            session['admin_username'] = username
            flash('Welcome, Admin!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials!', 'danger')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_loggedin' not in session:
        flash('Please login as admin first!', 'warning')
        return redirect(url_for('admin_login'))
    
    try:
       
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT u.*, 
                  (SELECT COUNT(*) 
                   FROM portfolio p 
                   WHERE p.user_id = u.user_id) AS portfolio_count
            FROM user u
        """)
        users = cursor.fetchall()
        
      
        user_count = len(users)
        
      
        cursor.execute("""
            SELECT COUNT(*) as user_count 
            FROM (
                SELECT DISTINCT user_id 
                FROM portfolio
            ) AS users_with_portfolios
        """)
        portfolio_stats = cursor.fetchone()
        
        cursor.close()
        
        return render_template('admin_dashboard.html', 
                              users=users, 
                              user_count=user_count,
                              portfolio_stats=portfolio_stats)
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('admin_login'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_loggedin', None)
    session.pop('admin_username', None)
    flash('You have been logged out from admin.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    setup_database()  # Setup database tables before running the app
    
    # Explicitly verify the dividends table
    verify_dividends_table()
    
    # Explicitly verify and update the transactions table
    verify_transactions_table()
    
    # Explicitly create watchlist table
    try:
        cursor = mysql.connection.cursor()
        print("Creating watchlist table...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS watchlist (
                watchlist_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                ticker_symbol VARCHAR(20) NOT NULL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                UNIQUE (user_id, ticker_symbol)
            )
        ''')
        mysql.connection.commit()
        cursor.close()
        print("Watchlist table created successfully!")
    except Exception as e:
        print(f"Error creating watchlist table: {str(e)}")
        
    app.run(debug=True)
