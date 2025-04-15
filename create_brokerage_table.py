import mysql.connector

print("Creating brokerage table...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Dropping existing brokerage table if it exists...")
    cursor.execute("DROP TABLE IF EXISTS brokerage")
    conn.commit()
    print("Existing table dropped (if any)")
    print("Creating new brokerage table...")
    cursor.execute()
    conn.commit()
    print("Brokerage table created successfully!")
    print("\nAdding a sample fee structure...")
    cursor.execute()
    conn.commit()
    print("Sample fee structure added")
    print("\nVerifying table structure:")
    cursor.execute("DESCRIBE brokerage")
    columns = cursor.fetchall()
    for col in columns:
        print(f"- {col[0]} ({col[1]})")
    print("\nVerifying data:")
    cursor.execute("SELECT * FROM brokerage")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print(f"ERROR: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 