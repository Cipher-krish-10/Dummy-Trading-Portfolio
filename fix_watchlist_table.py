import mysql.connector
import sys

print("\n*** Script starting: fix_watchlist_table.py ***")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    print("Connecting to database...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    print("Connected successfully!")
    print("\nChecking if watchlist table exists...")
    cursor.execute("SHOW TABLES LIKE 'watchlist'")
    watchlist_exists = cursor.fetchone() is not None
    print(f"Watchlist table exists: {watchlist_exists}")

    if watchlist_exists:
        cursor.execute("DESCRIBE watchlist")
        columns = cursor.fetchall()
        column_names = [col['Field'] for col in columns]
        print(f"\nCurrent watchlist columns: {column_names}")
        if 'ticker_symbol' not in column_names:
            print("\nThe ticker_symbol column is missing!")
            potential_columns = ['ticker', 'symbol', 'stock_symbol']
            existing_alt = None

            for col in potential_columns:
                if col in column_names:
                    existing_alt = col
                    print(f"Found alternative column: {col}")
                    break

            if existing_alt:
                print(f"\nRenaming column {existing_alt} to ticker_symbol...")
                try:
                    cursor.execute(f"ALTER TABLE watchlist CHANGE {existing_alt} ticker_symbol VARCHAR(20) NOT NULL")
                    conn.commit()
                    print("Column renamed successfully!")
                except Exception as e:
                    print(f"Error renaming column: {str(e)}")
            else:
                print("\nAdding ticker_symbol column...")
                try:
                    cursor.execute("ALTER TABLE watchlist ADD COLUMN ticker_symbol VARCHAR(20) NOT NULL")
                    conn.commit()
                    print("Column added successfully!")
                except Exception as e:
                    print(f"Error adding column: {str(e)}")
        if 'notes' not in column_names:
            print("\nThe notes column is missing!")
            print("Adding notes column...")
            try:
                cursor.execute("ALTER TABLE watchlist ADD COLUMN notes TEXT")
                conn.commit()
                print("Notes column added successfully!")
            except Exception as e:
                print(f"Error adding notes column: {str(e)}")
    else:
        print("\nCreating watchlist table...")
        try:
            cursor.execute()
            conn.commit()
            print("Watchlist table created successfully!")
        except Exception as e:
            print(f"Error creating watchlist table: {str(e)}")
    print("\nVerifying watchlist table structure...")
    cursor.execute("DESCRIBE watchlist")
    columns = cursor.fetchall()
    column_names = [col['Field'] for col in columns]
    print(f"Current watchlist columns: {column_names}")

    cursor.close()
    conn.close()
    print("\nScript completed successfully!")

except Exception as e:
    print(f"\nERROR: {str(e)}")
    sys.exit(1) 