
from app import app

if __name__ == '__main__':
    with app.app_context():
        from app import setup_database, verify_dividends_table, verify_transactions_table
        try:
            setup_database()
        except Exception as e:
            print(f"Database setup warning (non-fatal): {str(e)}")
        try:
            verify_dividends_table()
        except Exception as e:
            print(f"Warning - dividends table check: {str(e)}")

        try:
            verify_transactions_table()
        except Exception as e:
            print(f"Warning - transactions table check: {str(e)}")
    app.run(debug=True) 