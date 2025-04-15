import mysql.connector

print("Adding brokerage fee structures...")
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
    if not cursor.fetchone():
        print("Creating brokerage table...")
        cursor.execute()
        print("Brokerage table created!")
    cursor.execute("SELECT broker_id, broker_name FROM broker")
    brokers = cursor.fetchall()

    if not brokers:
        print("No brokers found. Please add brokers first.")
        exit(1)
    brokerage_structures = [
        (1, 0.00, 10000.00, 0.65, 6.95),     
        (1, 10000.01, 50000.00, 0.45, 4.95), 
        (1, 50000.01, 999999999.99, 0.30, 2.95), 
        (2, 0.00, 5000.00, 0.75, 7.99),     
        (2, 5000.01, 25000.00, 0.50, 6.99),  
        (2, 25000.01, 999999999.99, 0.35, 4.99), 
        (3, 0.00, 50000.00, 0.20, 0.00),    
        (3, 50000.01, 999999999.99, 0.10, 0.00)  
    ]
    cursor.execute("DELETE FROM brokerage")
    for structure in brokerage_structures:
        broker_id, min_amount, max_amount, percentage, flat_fee = structure

        cursor.execute(, (broker_id, min_amount, max_amount, percentage, flat_fee))

        broker_name = next((broker['broker_name'] for broker in brokers if broker['broker_id'] == broker_id), 'Unknown')
        print(f"Added fee structure for {broker_name}: {percentage}% + ${flat_fee} flat for transactions ${min_amount}-${max_amount}")
    conn.commit()
    cursor.execute()

    fee_structures = cursor.fetchall()

    print("\nCurrent brokerage fee structures:")
    current_broker = None

    for fee in fee_structures:
        if current_broker != fee['broker_name']:
            current_broker = fee['broker_name']
            print(f"\n{current_broker}:")

        print(f"  ${fee['min_amount']:.2f} - ${fee['max_amount']:.2f}: {fee['brokerage_percentage']}% + ${fee['flat_fee']:.2f} flat fee")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 