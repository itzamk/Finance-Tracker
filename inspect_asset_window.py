# inspect_asset_window.py

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from investment_database import get_asset_details, get_transaction_details, delete_transaction
from add_transaction_window import AddTransactionWindow
from modify_transaction_window import ModifyTransactionWindow
import datetime
from coingecko import fetch_price_history

class InspectAssetWindow(tk.Toplevel):
    def __init__(self, master, asset_id, app):
        super().__init__(master)
        self.app = app

        self.asset_details, self.transaction_history = get_asset_details(asset_id)
        self.title(f"Inspecting {self.asset_details[1]}")

        # Title Frame spanning across both columns
        self.title_frame = ttk.Frame(self)
        self.title_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        # Title Label
        self.asset_name_label = tk.Label(self.title_frame, text=f'{self.asset_details[1]} Overview\t\t\t ${self.asset_details[3]:,.2f}', font=("Arial", 24, "bold"))
        self.asset_name_label.pack(pady=(10, 0))

        # Top Left Quadrant: Container Frame
        self.left_container = ttk.Frame(self)
        self.left_container.grid(row=1, column=0, sticky="nsew")

        # Asset Details Frame
        self.details_frame = ttk.Frame(self.left_container)
        self.details_frame.pack(fill="both", expand=True)

        self.asset_name_label = ttk.Label(self.details_frame, text='\nInfo', font=("Arial", 16, "bold"))
        self.asset_name_label.pack()

        self.amount_label = ttk.Label(self.details_frame, text=f"\nAmount Holding: {self.asset_details[2]}")
        self.amount_label.pack()

        self.price_label = ttk.Label(self.details_frame, text=f"\nCurrent Price: ${self.asset_details[3]:,.2f}")
        self.price_label.pack()

        self.value_label = ttk.Label(self.details_frame, text=f"\nTotal Value: ${self.asset_details[2]*self.asset_details[3]:,.2f}")
        self.value_label.pack()

        self.cost_label = ttk.Label(self.details_frame, text=f"\nTotal Cost: ${self.calculate_metrics()[0]:,.2f}")
        self.cost_label.pack()

        self.gains_label = ttk.Label(self.details_frame, text=f"\nUnrealized: ${self.calculate_metrics()[1]:,.2f}")
        self.gains_label.pack()

        self.roi_label = ttk.Label(self.details_frame, text=f"\nROI: {self.calculate_metrics()[2]:.2f}%")
        self.roi_label.pack()

        # Buttons Frame
        self.button_frame = ttk.Frame(self.left_container)  # Parent is now self.left_container
        self.button_frame.pack(fill="x")  # Filling along the x-axis to take full width

        # Create and pack/grid the buttons within the button frame
        self.modify_button = ttk.Button(self.button_frame, text="Modify", command=self.open_modify_transaction_window)
        self.modify_button.grid(row=0, column=0, padx=5, pady=5)  # Added pady for spacing

        self.add_button = ttk.Button(self.button_frame, text="Add", command=self.open_add_transaction_window)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)  # Added pady for spacing

        self.delete_button = ttk.Button(self.button_frame, text="Delete", command=self.delete_selected_transaction)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)  # Added pady for spacing
        
        # Top Right Quadrant: Price Chart
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.grid(row=1, column=1, sticky="nsew")

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.update_chart()
        # Bottom Half: Transactions Table
        self.transactions_frame = ttk.Frame(self)
        self.transactions_frame.grid(row=2, columnspan=2, sticky="nsew")

        self.tree = ttk.Treeview(self.transactions_frame, columns=('Date', 'Price', 'Amount', 'Type'), show='headings')
        self.tree.heading('Date', text='Transaction Date')
        self.tree.heading('Price', text='Transaction Price')
        self.tree.heading('Amount', text='Transaction Amount')
        self.tree.heading('Type', text='Transaction Type')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for transaction in self.transaction_history:
            self.tree.insert('', 'end', values=(transaction[1], transaction[2], transaction[3], transaction[4]), tags=(transaction[0]))

    def update_chart(self):
        price_history_data = fetch_price_history(self.asset_details[0])
        if price_history_data is None:
            return  # Exit the function if price history data couldn't be fetched
        
        # Extracting dates and prices from price_history.strftime('%Y-%m-%d')
        price_history = price_history_data['prices']
        dates = [datetime.datetime.utcfromtimestamp(item[0] / 1000) for item in price_history]
        historical_prices = [item[1] for item in price_history]
        
        # Assume each item in transaction_history has the structure [transaction_date, transaction_price, transaction_amount, transaction_type]
        # where transaction_type is either 'buy' or 'sell'
        transaction_history = self.transaction_history
        total_amount_input = [0] * len(dates)
        unrealized_gains = [0] * len(dates)
        daily_value = [0] * len(dates)
        total_cost = 0
        total_amount = 0

        for i, date in enumerate(dates):
            date_obj = date.date() #datetime.datetime.strptime(date, '%Y-%m-%d')
            total_cost = 0
            total_amount = 0
            for transaction in transaction_history:
                transaction_date = datetime.datetime.strptime(transaction[1], '%m/%d/%y').date()
                if transaction_date <= date_obj:
                    if transaction[4] == 'buy':
                        total_cost += transaction[2] * transaction[3]
                        total_amount += transaction[3]
                    elif transaction[4] == 'sell':
                        total_cost -= transaction[2] * transaction[3]
                        total_amount -= transaction[3]
            # Update total_amount_input and unrealized_gains once per date
            total_amount_input[i] = total_cost
            daily_value[i] = total_amount * historical_prices[i]
            unrealized_gains[i] = daily_value[i] - total_cost

        # plot the total_amount_input and unrealized_gains
        self.ax.clear()
        self.ax.plot(dates, total_amount_input, label='Total Cost')
        self.ax.plot(dates, daily_value, label='Total Value')
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) 
        plt.xticks(rotation=-45)  # Rotate x-axis labels by 45 degrees
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Value (USD)')
        self.ax.set_title('Cost and Value Over Time')
        self.ax.legend()
        self.canvas.draw()

    def open_add_transaction_window(self):
            AddTransactionWindow(self, self.asset_details[0], self.app, update_callback=self.update_transactions)

    def open_modify_transaction_window(self):
        selected_item = self.tree.selection()
        
        if selected_item:
            transaction_id = self.tree.item(selected_item, 'tags')[0][0]
            transaction_details = get_transaction_details(transaction_id)
            if transaction_details:
                ModifyTransactionWindow(self, self.asset_details[0], transaction_details, self.app, update_callback=self.update_transactions)
            else:
                tk.messagebox.showerror("Error", "Could not find the transaction details.", parent=self)
        
        else:
            tk.messagebox.showwarning("No Selection", "No transaction selected. Please select a transaction to modify.", parent=self)

    def delete_selected_transaction(self):
        selected_item = self.tree.selection()
        if selected_item:
            transaction_id = self.tree.item(selected_item, 'tags')[0][0]
            delete_transaction(transaction_id)
            self.update_transactions()  # Update the transactions list
        else:
            tk.messagebox.showwarning("No Selection", "No transaction selected. Please select a transaction to delete.", parent=self)
            
        # self.app.update_ui()
        # self.update_transactions()

    def update_asset_details(self):
        self.asset_details, self.transaction_history = get_asset_details(self.asset_details[0])
        total_cost, unrealized_gains, roi = self.calculate_metrics()

        self.amount_label.config(text=f"\nAmount Holding: {self.asset_details[2]}")
        self.price_label.config(text=f"\nCurrent Price: ${self.asset_details[3]:,.2f}")
        self.value_label.config(text=f"\nTotal Value: ${self.asset_details[2]*self.asset_details[3]:,.2f}")
        self.cost_label.config(text=f'\nTotal Cost: ${total_cost:,.2f}')
        self.gains_label.config(text=f'\nUnrealized: ${unrealized_gains:,.2f}')
        self.roi_label.config(text=f'\nROI: {roi:.2f}%')

    def update_transactions(self):
        # Clear existing rows in the transactions list
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Get updated transactions data from the database
        asset_details, transaction_history = get_asset_details(self.asset_details[0])
        
        # Insert updated transactions data into the transactions list
        for transaction in transaction_history:
            self.tree.insert('', 'end', values=(transaction[1], transaction[2], transaction[3], transaction[4]), tags=(transaction[0]))

        self.calculate_metrics()
        self.update_asset_details()
        self.update_chart()
        self.app.update_ui()

    def calculate_metrics(self):
        total_cost = 0
        total_amount = 0

        for transaction in self.transaction_history:
            if transaction[4] == 'buy':
                total_cost += transaction[2] * transaction[3]  # price * amount
                total_amount += transaction[3]  # amount
            elif transaction[4] == 'sell':
                total_cost -= transaction[2] * transaction[3]  # price * amount
                total_amount -= transaction[3]  # amount

        unrealized_gains = total_amount * self.asset_details[3] - total_cost  # Assume current_price is known
        roi = (unrealized_gains / total_cost) * 100 if total_cost != 0 else 0  # Protect against division by zero

        return total_cost, unrealized_gains, roi
