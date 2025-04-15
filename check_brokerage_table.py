import mysql.connector

print("Checking brokerage table structure...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SHOW TABLES LIKE 'brokerage'")
    table_exists = cursor.fetchone() is not None

    if not table_exists:
        print("Brokerage table does not exist")
    else:
        cursor.execute("DESCRIBE brokerage")
        columns = cursor.fetchall()

        print("\nBrokerage table columns:")
        for col in columns:
            print(f"- {col['Field']} ({col['Type']})")
        cursor.execute("SELECT * FROM brokerage LIMIT 5")
        rows = cursor.fetchall()

        if rows:
            print("\nSample brokerage data:")
            for row in rows:
                print(row)
        else:
            print("\nNo data in brokerage table")
    print("\nChecking broker table for reference:")
    cursor.execute("SELECT broker_id, broker_name FROM broker")
    brokers = cursor.fetchall()

    if brokers:
        print("\nBrokers available:")
        for broker in brokers:
            print(f"- ID: {broker['broker_id']}, Name: {broker['broker_name']}")
    else:
        print("No brokers found")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 