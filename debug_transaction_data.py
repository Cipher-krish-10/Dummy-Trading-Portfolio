import mysql.connector

print("Debugging transaction data...")
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
    cursor.execute()

    stats = cursor.fetchone()
    print(f"\nTransactions statistics:")
    print(f"- Total transactions: {stats['total']}")
    print(f"- Transactions with NULL broker_id: {stats['null_broker']}")
    print(f"- Transactions with NULL/zero brokerage_fee: {stats['zero_fee']}")
    cursor.execute()

    transactions = cursor.fetchall()
    print("\nSample transactions:")
    for t in transactions:
        print(f"ID: {t['transaction_id']}, Symbol: {t['ticker_symbol']}")
        print(f"  Broker ID: {t['broker_id'] or 'NULL'}")
        print(f"  Broker Name: {t['broker_name'] or 'NULL'}")
        print(f"  Brokerage %: {t['brokerage_percentage'] or 'NULL'}")
        print(f"  Fee: {t['brokerage_fee'] or 'NULL'}")
        print("---")
    cursor.execute()
    cursor.execute()

    update_count = 0
    for t in cursor.fetchall():
        transaction_id = t['transaction_id']
        total_amount = t['quantity'] * t['price']
        percentage = t['brokerage_percentage'] or 0
        fee = total_amount * (percentage / 100)
        fee = round(fee, 2)
        cursor.execute(, (fee, transaction_id))

        update_count += 1

    conn.commit()
    print(f"\nUpdated brokerage fees for {update_count} transactions")
    cursor.execute()

    stats = cursor.fetchone()
    print(f"\nAfter fixes:")
    print(f"- Total transactions: {stats['total']}")
    print(f"- Transactions with NULL broker_id: {stats['null_broker']}")
    print(f"- Transactions with NULL/zero brokerage_fee: {stats['zero_fee']}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 