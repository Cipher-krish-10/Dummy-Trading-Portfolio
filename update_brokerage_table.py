import mysql.connector

print("Updating brokerage table structure...")
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
    print("Creating brokerage table with updated structure...")
    cursor.execute()

    print("Brokerage table created successfully!")
    print("Adding brokerage fee structures...")
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
    for structure in brokerage_structures:
        broker_id, min_amount, max_amount, percentage, flat_fee = structure

        try:
            cursor.execute(, (broker_id, min_amount, max_amount, percentage, flat_fee))
            print(f"Added fee structure: Broker ID {broker_id}, {percentage}% + ${flat_fee} flat for transactions ${min_amount}-${max_amount}")
        except Exception as e:
            print(f"Error adding fee for broker ID {broker_id}: {str(e)}")
    conn.commit()
    print("Changes committed to database")
    cursor.execute("DESCRIBE brokerage")
    columns = cursor.fetchall()

    print("\nVerified brokerage table structure:")
    for col in columns:
        field = col[0]
        data_type = col[1]
        print(f"- {field} ({data_type})")
    cursor.execute("SELECT COUNT(*) FROM brokerage")
    count = cursor.fetchone()[0]
    print(f"\nTotal brokerage fee structures added: {count}")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 