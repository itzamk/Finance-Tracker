# Import necessary libraries
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
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
        self.bills_table = ttk.Treeview(self.tab1, columns=('Name', 'Amount', 'Due Date'), show='headings')
        self.bills_table.heading('Name', text='Name')
        self.bills_table.heading('Amount', text='Amount')
        self.bills_table.heading('Due Date', text='Due Date')
        self.bills_table.pack(fill=tk.BOTH, expand=True)
        self.refresh_bills_button = ttk.Button(self.tab1, text='Refresh', command=self.refresh_bills)
        self.refresh_bills_button.pack(pady=10)

        # Investment Tracking Tab
        self.inv_name_entry = ttk.Entry(self.tab2)
        self.inv_name_entry.pack(pady=10)
        self.inv_amount_entry = ttk.Entry(self.tab2)
        self.inv_amount_entry.pack(pady=10)
        self.inv_date_entry = ttk.Entry(self.tab2)
        self.inv_date_entry.pack(pady=10)
        self.inv_value_entry = ttk.Entry(self.tab2)
        self.inv_value_entry.pack(pady=10)
        self.add_inv_button = ttk.Button(self.tab2, text='Add Investment', command=self.add_investment)
        self.add_inv_button.pack(pady=10)
        self.investments_table = ttk.Treeview(self.tab2, columns=('Name', 'Amount', 'Date', 'Current Value'), show='headings')
        self.investments_table.heading('Name', text='Name')
        self.investments_table.heading('Amount', text='Amount')
        self.investments_table.heading('Date', text='Date')
        self.investments_table.heading('Current Value', text='Current Value')
        self.investments_table.pack(fill=tk.BOTH, expand=True)
        self.refresh_investments_button = ttk.Button(self.tab2, text='Refresh', command=self.refresh_investments)
        self.refresh_investments_button.pack(pady=10)
        
        # Recurring Subscriptions Tab
        self.sub_name_entry = ttk.Entry(self.tab3)
        self.sub_name_entry.pack(pady=10)
        self.sub_amount_entry = ttk.Entry(self.tab3)
        self.sub_amount_entry.pack(pady=10)
        self.sub_renewal_date_entry = ttk.Entry(self.tab3)
        self.sub_renewal_date_entry.pack(pady=10)
        self.add_sub_button = ttk.Button(self.tab3, text='Add Subscription', command=self.add_subscription)
        self.add_sub_button.pack(pady=10)
        self.subscriptions_table = ttk.Treeview(self.tab3, columns=('Name', 'Amount', 'Renewal Date'), show='headings')
        self.subscriptions_table.heading('Name', text='Name')
        self.subscriptions_table.heading('Amount', text='Amount')
        self.subscriptions_table.heading('Renewal Date', text='Renewal Date')
        self.subscriptions_table.pack(fill=tk.BOTH, expand=True)
        self.refresh_subscriptions_button = ttk.Button(self.tab3, text='Refresh', command=self.refresh_subscriptions)
        self.refresh_subscriptions_button.pack(pady=10)



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

    def add_investment(self):
        name = self.inv_name_entry.get()
        amount = self.inv_amount_entry.get()
        date = self.inv_date_entry.get()
        current_value = self.inv_value_entry.get()
        
        c.execute("INSERT INTO investments VALUES (:name, :amount, :date, :current_value)",
                  {'name': name, 'amount': amount, 'date': date, 'current_value': current_value})
        conn.commit()
        
        messagebox.showinfo('Added', 'Investment added successfully')

    def add_subscription(self):
        name = self.sub_name_entry.get()
        amount = self.sub_amount_entry.get()
        renewal_date = self.sub_renewal_date_entry.get()
        
        c.execute("INSERT INTO subscriptions VALUES (:name, :amount, :renewal_date)",
                  {'name': name, 'amount': amount, 'renewal_date': renewal_date})
        conn.commit()
        
        messagebox.showinfo('Added', 'Subscription added successfully')

    def refresh_bills(self):
        for row in self.bills_table.get_children():
            self.bills_table.delete(row)
        c.execute("SELECT * FROM bills")
        for row in c.fetchall():
            self.bills_table.insert('', 'end', values=row)

    def refresh_investments(self):
        for row in self.investments_table.get_children():
            self.investments_table.delete(row)
        c.execute("SELECT * FROM investments")
        for row in c.fetchall():
            self.investments_table.insert('', 'end', values=row)

    def refresh_subscriptions(self):
        for row in self.subscriptions_table.get_children():
            self.subscriptions_table.delete(row)
        c.execute("SELECT * FROM subscriptions")
        for row in c.fetchall():
            self.subscriptions_table.insert('', 'end', values=row)

# Define the function to run when the application is closed
def on_closing():
    conn.close()  # Close the database connection
    app.destroy()  # Destroy the application window

if __name__ == '__main__':
    app = FinanceTracker()  # Create an instance of the FinanceTracker class
    app.protocol("WM_DELETE_WINDOW", on_closing)  # Set the function to run when the application is closed
    app.mainloop()  # Run the application
