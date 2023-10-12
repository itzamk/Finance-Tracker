import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3

# Connect to the database
conn = sqlite3.connect('finance.db')
c = conn.cursor()

# Create investments table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS investments (name TEXT, amount REAL, date TEXT, current_value REAL)''')
conn.commit()

class InvestmentTracker(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title('Investment Tracker')  # Set the title of the window
        self.geometry('800x600')  # Set the size of the window

        for col in range(2):  # There are two columns in the grid layout
            self.grid_columnconfigure(col, weight=1)  # Allow column resizing
        for row in range(8):  # There are eight rows in the grid layout
            self.grid_rowconfigure(row, weight=1)  # Allow row resizing
        
        # Create entry fields and labels for investment data
        ttk.Label(self, text="Investment Name:").grid(column=0, row=0, padx=10, pady=10)
        self.inv_name_entry = ttk.Entry(self)
        self.inv_name_entry.grid(column=0, row=1, padx=10, pady=10)
        
        ttk.Label(self, text="Amount:").grid(column=0, row=2, padx=10, pady=10)
        self.inv_amount_entry = ttk.Entry(self)
        self.inv_amount_entry.grid(column=0, row=3, padx=10, pady=10)
        
        ttk.Label(self, text="Date:").grid(column=0, row=4, padx=10, pady=10)
        self.inv_date_entry = ttk.Entry(self)
        self.inv_date_entry.grid(column=0, row=5, padx=10, pady=10)
        
        ttk.Label(self, text="Current Value:").grid(column=0, row=6, padx=10, pady=10)
        self.inv_value_entry = ttk.Entry(self)
        self.inv_value_entry.grid(column=0, row=7, padx=10, pady=10)
        
        # Create 'Add Investment' button
        self.add_inv_button = ttk.Button(self, text='Add Investment', command=self.add_investment)
        self.add_inv_button.grid(column=0, row=4, padx=10, pady=10)
        
        # Create table to display investments
        self.inv_table = ttk.Treeview(self, columns=('Name', 'Amount', 'Date', 'Current Value'), show='headings')
        self.inv_table.heading('Name', text='Name')
        self.inv_table.heading('Amount', text='Amount')
        self.inv_table.heading('Date', text='Date')
        self.inv_table.heading('Current Value', text='Current Value')
        self.inv_table.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky='nsew')  # Make the Treeview resizable
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.inv_table.yview)
        self.scrollbar.grid(column=2, row=5, sticky='ns')
        self.inv_table.configure(yscrollcommand=self.scrollbar.set)
        
        # Create 'Refresh', 'Modify' and 'Delete' buttons
        self.refresh_button = ttk.Button(self, text='Refresh', command=self.refresh_investments)
        self.refresh_button.grid(column=0, row=6, padx=10, pady=10)
        self.modify_button = ttk.Button(self, text='Modify', command=self.modify_investment)
        self.modify_button.grid(column=1, row=6, padx=10, pady=10)
        self.delete_button = ttk.Button(self, text='Delete', command=self.delete_investment)
        self.delete_button.grid(column=1, row=7, padx=10, pady=10)

    def add_investment(self):
        name = self.inv_name_entry.get()
        amount = self.inv_amount_entry.get()
        date = self.inv_date_entry.get()
        current_value = self.inv_value_entry.get()
        
        c.execute("INSERT INTO investments VALUES (:name, :amount, :date, :current_value)",
                  {'name': name, 'amount': amount, 'date': date, 'current_value': current_value})
        conn.commit()
        
        messagebox.showinfo('Added', 'Investment added successfully')

    def refresh_investments(self):
        for row in self.inv_table.get_children():
            self.inv_table.delete(row)
        c.execute("SELECT * FROM investments")
        for row in c.fetchall():
            self.inv_table.insert('', 'end', values=row)

    def modify_investment(self):
        selected_item = self.inv_table.selection()  # Get selected item
        if selected_item:
            old_data = self.inv_table.item(selected_item)['values']
            new_name = tk.simpledialog.askstring("Input", "Enter new investment name:", initialvalue=old_data[0])
            new_amount = tk.simpledialog.askstring("Input", "Enter new amount:", initialvalue=old_data[1])
            new_date = tk.simpledialog.askstring("Input", "Enter new date:", initialvalue=old_data[2])
            new_value = tk.simpledialog.askstring("Input", "Enter new current value:", initialvalue=old_data[3])
            
            c.execute('''UPDATE investments SET name = ?, amount = ?, date = ?, current_value = ? WHERE name = ? AND amount = ? AND date = ? AND current_value = ?''',
                      (new_name, new_amount, new_date, new_value, old_data[0], old_data[1], old_data[2], old_data[3]))
            conn.commit()
            self.refresh_investments()
        else:
            messagebox.showwarning("No Selection", "No row selected. Please select a row to modify.")

    def delete_investment(self):
        selected_item = self.inv_table.selection()  # Get selected item
        if selected_item:
            data = self.inv_table.item(selected_item)['values']
            c.execute('''DELETE FROM investments WHERE name = ? AND amount = ? AND date = ? AND current_value = ?''', data)
            conn.commit()
            self.refresh_investments()
        else:
            messagebox.showwarning("No Selection", "No row selected. Please select a row to delete.")

def on_closing():
    conn.close()  # Close the database connection
    app.destroy()  # Destroy the application window

if __name__ == '__main__':
    app = InvestmentTracker()
    app.protocol("WM_DELETE_WINDOW", on_closing)  # Set the function to run when the application is closed
    app.mainloop()