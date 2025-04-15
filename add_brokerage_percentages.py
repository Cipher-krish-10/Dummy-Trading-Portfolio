import mysql.connector

print("Adding brokerage percentages for each broker...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT broker_id, broker_name FROM broker")
    brokers = cursor.fetchall()

    if not brokers:
        print("No brokers found. Please add brokers first.")
        exit(1)
    brokerage_data = {
        1: 0.65,  
        2: 0.75,  
        3: 0.20   
    }
    cursor.execute("SHOW TABLES LIKE 'brokerage'")
    if not cursor.fetchone():
        print("Creating brokerage table with simplified structure...")
        cursor.execute()
        print("Brokerage table created!")
    cursor.execute("DELETE FROM brokerage")
    for broker in brokers:
        broker_id = broker['broker_id']
        percentage = brokerage_data.get(broker_id, 0.50)  
        cursor.execute(, (broker_id, percentage, percentage))

        print(f"Set {broker['broker_name']} (ID: {broker_id}) brokerage fee to {percentage}%")
    conn.commit()
    cursor.execute()

    broker_fees = cursor.fetchall()

    print("\nBrokerage percentages:")
    for broker in broker_fees:
        percentage = broker['brokerage_percentage'] if broker['brokerage_percentage'] else "Not set"
        print(f"- {broker['broker_name']}: {percentage}%")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 