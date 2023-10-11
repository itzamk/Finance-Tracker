# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Create tables for bills, investments, and subscriptions
c.execute('''CREATE TABLE IF NOT EXISTS bills (name TEXT, amount REAL, due_date TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS investments (name TEXT, amount REAL, date TEXT, current_value REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS subscriptions (name TEXT, amount REAL, renewal_date TEXT)''')

# Commit the changes and close the connection
conn.commit()

class FinanceTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Finance Tracker')  # Set the title of the window
        self.geometry('800x600')  # Set the size of the window
        
        # Create a tab control with three tabs
        self.tab_control = ttk.Notebook(self)
        
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        
        # Name the tabs
        self.tab_control.add(self.tab1, text='Bill Reminders')
        self.tab_control.add(self.tab2, text='Investment Tracking')
        self.tab_control.add(self.tab3, text='Recurring Subscriptions')
        
        # Display the tab control
        self.tab_control.pack(expand=1, fill='both')
        
        # Bill Reminders Tab
        self.bill_name_entry = ttk.Entry(self.tab1)  # Entry field for the bill name
        self.bill_name_entry.pack(pady=10)  # Display the entry field
        self.bill_amount_entry = ttk.Entry(self.tab1)  # Entry field for the bill amount
        self.bill_amount_entry.pack(pady=10)  # Display the entry field
        self.bill_due_date_entry = ttk.Entry(self.tab1)  # Entry field for the bill due date
        self.bill_due_date_entry.pack(pady=10)  # Display the entry field
        self.add_bill_button = ttk.Button(self.tab1, text='Add Bill', command=self.add_bill)  # Button to add a bill
        self.add_bill_button.pack(pady=10)  # Display the button

    def add_bill(self):
        # Get the data from the entry fields
        name = self.bill_name_entry.get()
        amount = self.bill_amount_entry.get()
        due_date = self.bill_due_date_entry.get()
        
        # Insert the data into the bills table
        c.execute("INSERT INTO bills VALUES (:name, :amount, :due_date)",
                  {'name': name, 'amount': amount, 'due_date': due_date})
        conn.commit()  # Commit the changes
        
        # Notify the user
        messagebox.showinfo('Added', 'Bill added successfully')

# Define the function to run when the application is closed
def on_closing():
    conn.close()  # Close the database connection
    app.destroy()  # Destroy the application window

if __name__ == '__main__':
    app = FinanceTracker()  # Create an instance of the FinanceTracker class
    app.protocol("WM_DELETE_WINDOW", on_closing)  # Set the function to run when the application is closed
    app.mainloop()  # Run the application
