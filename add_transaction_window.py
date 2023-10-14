import tkinter as tk
from investment_database import add_transaction
from tkcalendar import DateEntry

class AddTransactionWindow(tk.Toplevel):
    def __init__(self, master, asset_id, update_callback=None):
        super().__init__(master)

        self.update_callback = update_callback  # Store the callback
        
        self.title(f"Add Transaction")
        self.asset_id = asset_id

        self.date_label = tk.Label(self, text="Date:")
        self.date_label.grid(row=0, column=0)
        self.date_entry = DateEntry(self)
        self.date_entry.grid(row=0, column=1)

        self.price_label = tk.Label(self, text="Price:")
        self.price_label.grid(row=1, column=0)
        self.price_entry = tk.Entry(self)
        self.price_entry.grid(row=1, column=1)

        self.amount_label = tk.Label(self, text="Amount:")
        self.amount_label.grid(row=2, column=0)
        self.amount_entry = tk.Entry(self)
        self.amount_entry.grid(row=2, column=1)

        self.type_label = tk.Label(self, text="Type:")
        self.type_label.grid(row=3, column=0)
        self.type_combobox = tk.ttk.Combobox(self, values=["Buy", "Sell"])
        self.type_combobox.grid(row=3, column=1)

        self.add_button = tk.Button(self, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, columnspan=2)

    def add_transaction(self):
        date = self.date_entry.get()
        price = float(self.price_entry.get())
        amount = float(self.amount_entry.get())
        transaction_type = self.type_combobox.get().lower()

        # Add some validation here to ensure the inputs are valid?

        add_transaction(self.asset_id, date, price, amount, transaction_type)
        if self.update_callback:  # If a callback was provided, call it
            self.update_callback()
        self.destroy()  # Close the window after adding the transaction
