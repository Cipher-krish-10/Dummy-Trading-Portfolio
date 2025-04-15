import mysql.connector
import sys

print("\n*** Script starting: check_tables.py ***")
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

    print("\nListing all tables:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()

    for table in tables:
        table_name = list(table.values())[0]
        print(f"  - {table_name}")

    print("\nChecking if transactions table exists...")
    cursor.execute("SHOW TABLES LIKE 'transactions'")
    transactions_exists = cursor.fetchone() is not None
    print(f"Transactions table exists: {transactions_exists}")

    if not transactions_exists:
        print("\nCreating transactions table...")
        cursor.execute()
        conn.commit()
        print("Transactions table created!")
        cursor.execute("SHOW TABLES LIKE 'transactions'")
        print(f"Table exists now: {cursor.fetchone() is not None}")

    cursor.close()
    conn.close()
    print("\nScript completed successfully!")

except Exception as e:
    print(f"\nERROR: {str(e)}")
    sys.exit(1) 