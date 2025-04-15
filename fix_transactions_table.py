import mysql.connector

print("Starting fix_transactions_table.py script...")
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'krishuppal10',
    'database': 'dummy_portfolio'
}

def create_transactions_table():

    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor(dictionary=True)

        print("\n=== Creating transactions table ===")
        cursor.execute()

        conn.commit()
        print("Transactions table created successfully!")

    except Exception as e:
        print(f"Error creating transactions table: {str(e)}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    create_transactions_table() 