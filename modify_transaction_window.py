# modify_transaction_window.py

import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from investment_database import modify_transaction

class ModifyTransactionWindow(tk.Toplevel):
    def __init__(self, master, asset_id, transaction_details, app, update_callback=None):
        super().__init__(master)
        
        self.app = app
        self.update_callback = update_callback  # Store the callback
        
        self.title(f"Modify Transaction")
        self.asset_id = asset_id
        self.transaction_id = transaction_details[0]

        self.date_label = tk.Label(self, text="Date:")
        self.date_label.grid(row=0, column=0)
        self.date_entry = DateEntry(self)
        self.date_entry.grid(row=0, column=1)
        self.date_entry.set_date(transaction_details[1])

        self.price_label = tk.Label(self, text="Price:")
        self.price_label.grid(row=1, column=0)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1)
        self.price_entry.insert(0, transaction_details[2])

        self.amount_label = tk.Label(self, text="Amount:")
        self.amount_label.grid(row=2, column=0)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=2, column=1)
        self.amount_entry.insert(0, transaction_details[3])

        self.type_label = tk.Label(self, text="Type:")
        self.type_label.grid(row=3, column=0)
        self.type_combobox = tk.ttk.Combobox(self, values=["Buy", "Sell"])
        self.type_combobox.grid(row=3, column=1)
        self.type_combobox.set(transaction_details[4])

        self.modify_button = tk.Button(self, text="Modify Transaction", command=self.modify_transaction)
        self.modify_button.grid(row=4, columnspan=2)

    def modify_transaction(self):
        date = self.date_entry.get()
        price = float(self.price_entry.get())
        amount = float(self.amount_entry.get())
        transaction_type = self.type_combobox.get().lower()

        modify_transaction(self.transaction_id, date, price, amount, transaction_type)
        if self.update_callback:  # If a callback was provided, call it
            self.update_callback()

        self.app.update_ui()
        self.destroy()  # Close the window after modifying the transaction