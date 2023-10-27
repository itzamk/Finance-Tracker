# investment_database.py

import sqlite3
from coingecko import fetch_price, fetch_asset_info
import threading
import time

def setup_database():
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE IF NOT EXISTS investments
              (id TEXT PRIMARY KEY,
              name TEXT UNIQUE,
              amount REAL DEFAULT 0,
              current_price REAL,
              deleted INTEGER DEFAULT 0)
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS transactions
              (id INTEGER PRIMARY KEY,
              investment_id TEXT,
              transaction_date DATE,
              transaction_price REAL,
              transaction_amount REAL,
              transaction_type TEXT,
              FOREIGN KEY (investment_id) REFERENCES investments(id))
              ''')

    conn.commit()
    conn.close()

def add_new_asset(asset_id, asset_name):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()

        # Fetch the current price of the asset
        asset_info = fetch_asset_info(asset_id)

        query = '''INSERT INTO investments (id, name, current_price) VALUES (?, ?, ?)'''
        c.execute(query, (asset_id, asset_name, asset_info['price']))

        conn.commit()

    except sqlite3.IntegrityError:
        print(f"Asset {asset_name} already exists in the database.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        conn.close()

def get_asset_details(asset_id):
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()

    try:
        # Get asset details
        query = '''SELECT id, name, amount, current_price FROM investments WHERE id = ?'''
        c.execute(query, (asset_id,))
        asset_details = c.fetchone()

        # Get transaction history
        query = '''
                SELECT id, transaction_date, transaction_price, transaction_amount, transaction_type
                FROM transactions
                WHERE investment_id = ?
                ORDER BY transaction_date DESC
                '''
        
        c.execute(query, (asset_id,))
        transaction_history = c.fetchall()

        return asset_details, transaction_history

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_transaction_details(transaction_id):
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()
    
    try:
        query = '''
                SELECT id, transaction_date, transaction_price, transaction_amount, transaction_type 
                FROM transactions 
                WHERE id = ?
                '''
        c.execute(query, (transaction_id,))
        transaction_details = c.fetchone()
        return transaction_details
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        conn.close()

def update_total_holding(investment_id):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()

        # Adjust the transaction_amount for Sell transactions, then sum all transaction_amount values.
        c.execute('''
                  SELECT SUM(
                      CASE 
                          WHEN transaction_type = 'sell' THEN -transaction_amount
                          ELSE transaction_amount
                      END
                  ) 
                  FROM transactions 
                  WHERE investment_id = ?
                  ''', (investment_id,))
        total_holding = c.fetchone()[0]

        # Check if total_holding is None and set it to 0 if it is
        if total_holding is None:
            total_holding = 0

        # Now update the investments table with the new total_holding.
        c.execute('''
                  UPDATE investments 
                  SET amount = ? 
                  WHERE id = ?
                  ''', (total_holding, investment_id))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def add_transaction(investment_id, transaction_date, transaction_price, transaction_amount, transaction_type):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()

        query = '''
                INSERT INTO transactions (investment_id, transaction_date, transaction_price, transaction_amount, transaction_type)
                VALUES (?, ?, ?, ?, ?)
                '''
        c.execute(query, (investment_id, transaction_date, transaction_price, transaction_amount, transaction_type))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
    
    # Call update_total_holding after adding a transaction
    update_total_holding(investment_id)

def modify_transaction(transaction_id, new_date=None, new_price=None, new_amount=None, new_type=None):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        
        # Get the investment_id before modifying the transaction
        c.execute('SELECT investment_id FROM transactions WHERE id = ?', (transaction_id,))
        investment_id = c.fetchone()[0]

        if new_date:
            c.execute('UPDATE transactions SET transaction_date = ? WHERE id = ?', (new_date, transaction_id))
        if new_price:
            c.execute('UPDATE transactions SET transaction_price = ? WHERE id = ?', (new_price, transaction_id))
        if new_amount:
            c.execute('UPDATE transactions SET transaction_amount = ? WHERE id = ?', (new_amount, transaction_id))
        if new_type:
            c.execute('UPDATE transactions SET transaction_type = ? WHERE id = ?', (new_type, transaction_id))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
    
    # Call update_total_holding after adding a transaction
    update_total_holding(investment_id)

def delete_transaction(transaction_id):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        
        # Get the investment_id before deleting the transaction
        c.execute('SELECT investment_id FROM transactions WHERE id = ?', (transaction_id,))
        investment_id = c.fetchone()[0]

        c.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
    
    # Call update_total_holding after adding a transaction
    update_total_holding(investment_id)

def soft_delete_asset(asset_id):
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()
    
    c.execute('''
              UPDATE investments
              SET deleted = 1
              WHERE id = ?
              ''', (asset_id,))
    
    conn.commit()
    conn.close()

def restore_asset(asset_id):
    try:
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()

        c.execute('UPDATE investments SET deleted = 0 WHERE id = ?', (asset_id,))

        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

def get_deleted_assets():
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()
    
    c.execute('''
              SELECT * FROM investments
              WHERE deleted = 1
              ''')
    
    deleted_assets = c.fetchall()
    conn.close()
    return deleted_assets

def refresh_prices():
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()
    assets = c.execute('SELECT id FROM investments WHERE deleted = 0').fetchall()
    for asset in assets:
        current_price = fetch_price(asset[0])
        if current_price is not None:  # only update if fetch was successful
            c.execute('UPDATE investments SET current_price = ? WHERE id = ?', (current_price, asset[0]))
    conn.commit()
    conn.close()

def auto_refresh_prices(interval=600):  # Refresh every 10 minutes
    while True:
        refresh_prices()
        time.sleep(interval)

def start_auto_refresh():
    refresh_thread = threading.Thread(target=auto_refresh_prices)
    refresh_thread.daemon = True  # Daemonize the thread so it exits when the main program exits
    refresh_thread.start()