import mysql.connector

print("Creating full brokerage table with fee structures...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Dropping existing brokerage table...")
    cursor.execute("DROP TABLE IF EXISTS brokerage")
    conn.commit()
    print("Creating brokerage table...")
    cursor.execute()
    conn.commit()
    print("Brokerage table created!")
    print("\nInserting fee structures...")
    brokerage_structures = [
        (1, 0.00, 10000.00, 0.65, 6.95),     
        (1, 10000.01, 50000.00, 0.45, 4.95), 
        (1, 50000.01, 1000000.00, 0.30, 2.95), 
        (2, 0.00, 5000.00, 0.75, 7.99),     
        (2, 5000.01, 25000.00, 0.50, 6.99),  
        (2, 25000.01, 1000000.00, 0.35, 4.99), 
        (3, 0.00, 50000.00, 0.20, 0.00),    
        (3, 50000.01, 1000000.00, 0.10, 0.00)  
    ]
    cursor.execute("SELECT broker_id FROM broker")
    existing_brokers = [row[0] for row in cursor.fetchall()]
    print(f"Existing broker IDs: {existing_brokers}")
    insert_count = 0
    for structure in brokerage_structures:
        broker_id = structure[0]
        if broker_id in existing_brokers:
            cursor.execute(, structure)
            print(f"Added fee structure for broker ID {broker_id}: {structure[3]}% + ${structure[4]} flat fee for ${structure[1]}-${structure[2]}")
            insert_count += 1

    conn.commit()
    print(f"\nSuccessfully added {insert_count} fee structures")
    print("\nFee structures in database:")
    cursor.execute()

    fee_structures = cursor.fetchall()
    current_broker = None

    for fee in fee_structures:
        broker_name = fee[0]
        min_amt = fee[1]
        max_amt = fee[2]
        percentage = fee[3]
        flat_fee = fee[4]

        if current_broker != broker_name:
            current_broker = broker_name
            print(f"\n{current_broker}:")

        print(f"  ${min_amt:.2f} - ${max_amt:.2f}: {percentage}% + ${flat_fee:.2f} flat fee")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 