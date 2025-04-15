import mysql.connector
import sys
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',  
    'database': 'dummy_portfolio'
}

def check_and_fix_database():

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        print("\n=== Checking database structure ===")
        cursor.execute("SHOW TABLES LIKE 'portfolio'")
        if cursor.fetchone():
            print("\nInspecting portfolio table structure:")
            cursor.execute("DESCRIBE portfolio")
            columns = cursor.fetchall()
            column_names = [col['Field'] for col in columns]
            print(f"Current columns: {column_names}")
            if 'ticker_symbol' not in column_names:
                print("Column 'ticker_symbol' is missing! Altering table to add it...")
                try:
                    cursor.execute("ALTER TABLE portfolio ADD COLUMN ticker_symbol VARCHAR(20) NOT NULL DEFAULT 'AAPL'")
                    conn.commit()
                    cursor.execute("SHOW INDEX FROM portfolio WHERE Key_name = 'unique_user_stock'")
                    unique_exists = cursor.fetchone()

                    if not unique_exists:
                        try:
                            cursor.execute("ALTER TABLE portfolio ADD CONSTRAINT unique_user_stock UNIQUE (user_id, ticker_symbol)")
                            conn.commit()
                            print("Added unique constraint on user_id and ticker_symbol")
                        except Exception as e:
                            print(f"Warning: Could not add unique constraint: {e}")

                    print("Portfolio table structure updated.")
                except Exception as e:
                    print(f"Warning: Could not alter portfolio table: {e}")
                    print("Please manually fix your database structure to include a ticker_symbol column.")
                    print("Suggested SQL command:")
                    print("ALTER TABLE portfolio ADD COLUMN ticker_symbol VARCHAR(20) NOT NULL DEFAULT 'AAPL';")
                    print("ALTER TABLE portfolio ADD CONSTRAINT unique_user_stock UNIQUE (user_id, ticker_symbol);")
                cursor.execute("DESCRIBE portfolio")
                columns = cursor.fetchall()
                column_names = [col['Field'] for col in columns]
                print(f"Updated columns: {column_names}")
            if 'quantity' not in column_names:
                print("Column 'quantity' is missing! Adding it...")
                try:
                    cursor.execute("ALTER TABLE portfolio ADD COLUMN quantity INT DEFAULT 1")
                    conn.commit()
                    print("Added quantity column")
                except Exception as e:
                    print(f"Warning: Could not add quantity column: {e}")

            if 'added_date' not in column_names:
                print("Column 'added_date' is missing! Adding it...")
                try:
                    cursor.execute("ALTER TABLE portfolio ADD COLUMN added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                    conn.commit()
                    print("Added added_date column")
                except Exception as e:
                    print(f"Warning: Could not add added_date column: {e}")
        cursor.execute("SHOW TABLES LIKE 'user'")
        user_table_exists = cursor.fetchone() is not None
        print(f"User table exists: {user_table_exists}")

        if not user_table_exists:
            print("Creating user table...")
            cursor.execute()
            conn.commit()
        cursor.execute("SHOW TABLES LIKE 'STOCK'")
        stock_table_exists = cursor.fetchone() is not None
        print(f"STOCK table exists: {stock_table_exists}")

        if not stock_table_exists:
            print("Creating STOCK table...")
            cursor.execute()
            conn.commit()
        cursor.execute("SHOW TABLES LIKE 'portfolio'")
        portfolio_table_exists = cursor.fetchone() is not None
        print(f"Portfolio table exists: {portfolio_table_exists}")

        if not portfolio_table_exists:
            print("Creating portfolio table...")
            cursor.execute()
            conn.commit()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        print(f"\nUsers in database: {len(users)}")
        for user in users:
            print(f"  - User ID: {user['user_id']}, Username: {user['username']}")

        if not users:
            print("Adding test user...")
            cursor.execute()
            conn.commit()
        cursor.execute("SELECT * FROM portfolio")
        portfolios = cursor.fetchall()
        print(f"\nPortfolio entries: {len(portfolios)}")
        for entry in portfolios:
            print(f"  - Portfolio ID: {entry['portfolio_id']}, User ID: {entry['user_id']}, Stock: {entry.get('ticker_symbol', 'UNKNOWN')}, Quantity: {entry.get('quantity', 0)}")
        cursor.execute("SELECT COUNT(*) as count FROM STOCK")
        stock_count = cursor.fetchone()['count']

        if stock_count == 0:
            print("\nAdding sample stocks to STOCK table...")
            sample_stocks = [
                ('Apple Inc.', 'AAPL', 175.0, 'Technology'),
                ('Microsoft Corporation', 'MSFT', 350.0, 'Technology'),
                ('Amazon.com Inc.', 'AMZN', 180.0, 'Consumer Cyclical')
            ]

            for stock in sample_stocks:
                cursor.execute(, stock)
            conn.commit()
            print("Sample stocks added.")
        if users and not portfolios:
            print("\nAdding sample portfolio entries for test user...")
            user_id = users[0]['user_id']
            sample_portfolio = [
                (user_id, 'AAPL', 5),
                (user_id, 'MSFT', 2)
            ]

            for entry in sample_portfolio:
                cursor.execute(, entry)
            conn.commit()
            print("Sample portfolio entries added.")

        print("\n=== Database check and fix completed successfully ===")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    check_and_fix_database() 