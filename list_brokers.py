import mysql.connector

print("Listing all brokers...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT broker_id, broker_name FROM broker")
    rows = cursor.fetchall()

    print("\nBrokers in database:")
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
    else:
        print("No brokers found!")
    cursor.execute("SELECT COUNT(*) FROM broker")
    count = cursor.fetchone()[0]
    print(f"\nTotal broker count: {count}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 