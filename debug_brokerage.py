import mysql.connector

print("Debugging brokerage table issues...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION()")
    version = cursor.fetchone()
    print(f"MySQL Version: {version[0]}")
    print("\nExisting tables:")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"- {table[0]}")
    cursor.execute("SELECT COUNT(*) FROM broker")
    broker_count = cursor.fetchone()[0]
    print(f"\nBroker table has {broker_count} records")

    if broker_count > 0:
        cursor.execute("SELECT * FROM broker")
        brokers = cursor.fetchall()
        print("Broker records:")
        for broker in brokers:
            print(f"- {broker}")
    print("\nAttempting to create simplified brokerage table...")
    try:
        cursor.execute("DROP TABLE IF EXISTS brokerage")
        conn.commit()
        print("Dropped existing brokerage table (if any)")
    except Exception as e:
        print(f"Error dropping table: {str(e)}")
    try:
        cursor.execute()
        conn.commit()
        print("Created minimal brokerage table")
        cursor.execute("INSERT INTO brokerage (broker_id, fee) VALUES (1, 5.99)")
        conn.commit()
        print("Successfully inserted test record")
        cursor.execute("SELECT * FROM brokerage")
        rows = cursor.fetchall()
        print("Data in brokerage table:")
        for row in rows:
            print(f"- {row}")

    except Exception as e:
        print(f"Error creating simple table: {str(e)}")

except Exception as e:
    print(f"Database connection error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Debug script completed.") 