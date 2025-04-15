import mysql.connector

print("Checking transaction broker data...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    print("\nChecking transactions table structure:")
    cursor.execute("DESCRIBE transactions")
    columns = cursor.fetchall()

    for col in columns:
        print(f"- {col['Field']} ({col['Type']})")
    column_names = [col['Field'] for col in columns]
    has_broker_id = 'broker_id' in column_names
    has_brokerage_fee = 'brokerage_fee' in column_names

    print(f"\nHas broker_id column: {has_broker_id}")
    print(f"Has brokerage_fee column: {has_brokerage_fee}")
    cursor.execute()

    transactions = cursor.fetchall()

    print(f"\nFound {len(transactions)} transactions. Sample data:")

    for idx, t in enumerate(transactions):
        print(f"\nTransaction 
        print(f"  ID: {t['transaction_id']}")
        print(f"  Ticker: {t['ticker_symbol']}")
        print(f"  Type: {t['transaction_type']}")
        print(f"  Broker ID: {t['broker_id']}")
        print(f"  Broker Name: {t.get('broker_name', 'None')}")
        print(f"  Brokerage Fee: {t.get('brokerage_fee', 'None')}")
    cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE broker_id IS NULL")
    null_broker_count = cursor.fetchone()['count']

    print(f"\nTransactions with NULL broker_id: {null_broker_count}")
    if has_brokerage_fee:
        cursor.execute("SELECT COUNT(*) as count FROM transactions WHERE brokerage_fee = 0 OR brokerage_fee IS NULL")
        zero_fee_count = cursor.fetchone()['count']
        print(f"Transactions with zero/NULL brokerage_fee: {zero_fee_count}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 