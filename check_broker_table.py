import mysql.connector

print("Checking broker table structure...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("DESCRIBE broker")
    columns = cursor.fetchall()

    print("\nBroker table columns:")
    for column in columns:
        print(f"- {column['Field']} ({column['Type']})")
    cursor.execute("SELECT * FROM broker")
    rows = cursor.fetchall()

    print("\nAll broker data:")
    for row in rows:
        print(row)
    cursor.execute("SELECT COUNT(*) as count FROM broker")
    count = cursor.fetchone()['count']
    print(f"\nTotal broker count: {count}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 