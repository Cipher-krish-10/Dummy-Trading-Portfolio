import mysql.connector

print("Adding broker columns to transactions table...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Checking if columns already exist...")
    cursor.execute("DESCRIBE transactions")
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns]
    if 'broker_id' not in column_names:
        print("Adding broker_id column to transactions table...")
        cursor.execute("ALTER TABLE transactions ADD COLUMN broker_id INT")
        print("broker_id column added!")
    else:
        print("broker_id column already exists")
    if 'brokerage_fee' not in column_names:
        print("Adding brokerage_fee column to transactions table...")
        cursor.execute("ALTER TABLE transactions ADD COLUMN brokerage_fee DECIMAL(10, 2) DEFAULT 0")
        print("brokerage_fee column added!")
    else:
        print("brokerage_fee column already exists")
    conn.commit()
    print("Changes committed to database")
    cursor.execute("DESCRIBE transactions")
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns]

    print("\nVerifying transaction table structure:")
    for col in columns:
        print(f"- {col[0]} ({col[1]})")

    print(f"\nbroker_id in columns: {'broker_id' in column_names}")
    print(f"brokerage_fee in columns: {'brokerage_fee' in column_names}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 