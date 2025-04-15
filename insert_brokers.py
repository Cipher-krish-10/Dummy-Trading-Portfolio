import mysql.connector
import traceback

print("Starting to insert brokers...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    print("Connecting to database...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connected successfully!")
    brokers_to_add = [
        ('TD Ameritrade',),
        ('E*TRADE',),
        ('Vanguard',)
    ]
    insert_query = 

    print("Starting to add brokers...")
    for broker in brokers_to_add:
        try:
            cursor.execute(insert_query, broker)
            print(f"Added broker: {broker[0]}")
        except Exception as e:
            print(f"Error adding broker {broker[0]}: {str(e)}")
    conn.commit()
    print(f"Successfully added brokers to the database!")
    cursor.execute("SELECT broker_id, broker_name FROM broker")
    brokers = cursor.fetchall()
    print("\nCurrent brokers in database:")
    for broker in brokers:
        print(f"ID: {broker[0]}, Name: {broker[1]}")

except Exception as e:
    print(f"ERROR: {str(e)}")
    print(traceback.format_exc())
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("Database connection closed.")

print("Script completed.") 