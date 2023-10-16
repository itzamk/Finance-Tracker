import sqlite3

def add_deleted_column():
    conn = sqlite3.connect('investments.db')
    c = conn.cursor()
    
    # Add a new column 'deleted' to the investments table
    c.execute('''
              ALTER TABLE investments
              ADD COLUMN deleted INTEGER DEFAULT 0
              ''')
    conn.commit()
    conn.close()

# Call the function
add_deleted_column()