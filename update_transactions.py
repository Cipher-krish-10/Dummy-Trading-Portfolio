import mysql.connector
import random

print("Updating existing transactions with broker information...")
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
        print("No brokers found in the broker table. Please add brokers first.")
        exit(1)
    cursor.execute("SELECT transaction_id, transaction_type, price, quantity FROM transactions")
    transactions = cursor.fetchall()

    if not transactions:
        print("No transactions found.")
    else:
        print(f"Found {len(transactions)} transactions to update.")
        for transaction in transactions:
            broker = random.choice(brokers)
            value = float(transaction['price']) * transaction['quantity']
            fee_rate = random.uniform(0.005, 0.01)  
            brokerage_fee = round(value * fee_rate, 2)
            cursor.execute(, (broker['broker_id'], brokerage_fee, transaction['transaction_id']))

            print(f"Updated transaction {transaction['transaction_id']} with broker {broker['broker_name']} and fee ${brokerage_fee}")
        conn.commit()
        print(f"Successfully updated {len(transactions)} transactions.")

except Exception as e:
    print(f"Error: {str(e)}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\nDatabase connection closed.")

print("Script completed.") 