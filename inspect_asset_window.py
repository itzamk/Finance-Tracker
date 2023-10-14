import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from investment_database import get_asset_details, add_transaction, modify_transaction, delete_transaction
from add_transaction_window import AddTransactionWindow

class InspectAssetWindow(tk.Toplevel):
    def __init__(self, master, asset_name):
        super().__init__(master)
        self.title(f"Inspecting {asset_name}")

        self.asset_details, self.transaction_history = get_asset_details(asset_name)

        # Top Left Quadrant: Container Frame
        self.left_container = tk.Frame(self)
        self.left_container.grid(row=0, column=0, sticky="nsew")

        # Asset Details Frame
        self.details_frame = tk.Frame(self.left_container)
        self.details_frame.pack(fill="both", expand=True)

        self.asset_name_label = tk.Label(self.details_frame, text=asset_name, font=("Arial", 24, "bold"))
        self.asset_name_label.pack()

        self.amount_label = tk.Label(self.details_frame, text=f"Amount Holding: {self.asset_details[2]}")
        self.amount_label.pack()

        self.price_label = tk.Label(self.details_frame, text=f"Current Price: ${self.asset_details[3]:,.2f}")
        self.price_label.pack()

        self.value_label = tk.Label(self.details_frame, text=f"Total Value: ${self.asset_details[2]*self.asset_details[3]:,.2f}")
        self.value_label.pack()

        # Buttons Frame
        self.button_frame = tk.Frame(self.left_container)  # Parent is now self.left_container
        self.button_frame.pack(fill="x")  # Filling along the x-axis to take full width

        # Create and pack/grid the buttons within the button frame
        self.modify_button = tk.Button(self.button_frame, text="Modify", command=self.open_add_transaction_window)
        self.modify_button.grid(row=0, column=0, padx=5, pady=5)  # Added pady for spacing

        self.add_button = tk.Button(self.button_frame, text="Add", command=self.open_add_transaction_window)
        self.add_button.grid(row=1, column=0, padx=5, pady=5)  # Added pady for spacing

        self.delete_button = tk.Button(self.button_frame, text="Delete", command=self.delete_selected_transaction)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)  # Added pady for spacing

        # Top Right Quadrant: Dummy Chart
        self.chart_frame = tk.Frame(self)
        self.chart_frame.grid(row=0, column=1, sticky="nsew")

        self.fig, self.ax = plt.subplots()
        sizes = [15, 30, 45, 10]  # Dummy data for the pie chart
        labels = ['Dummy A', 'Dummy B', 'Dummy C', 'Dummy D']
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Bottom Half: Transactions Table
        self.transactions_frame = tk.Frame(self)
        self.transactions_frame.grid(row=1, columnspan=2, sticky="nsew")

        self.tree = ttk.Treeview(self.transactions_frame, columns=('Date', 'Price', 'Amount', 'Type'), show='headings')
        self.tree.heading('Date', text='Transaction Date')
        self.tree.heading('Price', text='Transaction Price')
        self.tree.heading('Amount', text='Transaction Amount')
        self.tree.heading('Type', text='Transaction Type')
        self.tree.pack(fill=tk.BOTH, expand=True)

        for transaction in self.transaction_history:
            self.tree.insert('', 'end', values=(transaction[1], transaction[2], transaction[3], transaction[4]), tags=(transaction[0],))

    def open_add_transaction_window(self):
            AddTransactionWindow(self, self.asset_details[0], update_callback=self.update_transactions)

    #def open_modify_transaction_window(self):
        # Open a new window to modify the selected transaction

    def delete_selected_transaction(self):
        selected_item = self.tree.selection()
        if selected_item:
            transaction_id = self.tree.item(selected_item, 'tags')[0][0]
            delete_transaction(transaction_id)
            self.update_transactions()  # Update the transactions list
        else:
            tk.messagebox.showwarning("No Selection", "No transaction selected. Please select a transaction to delete.")

    def update_transactions(self):
        # Clear existing rows in the transactions list
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Get updated transactions data from the database
        asset_details, transaction_history = get_asset_details(self.asset_details[1])
        
        # Insert updated transactions data into the transactions list
        for transaction in transaction_history:
            self.tree.insert('', 'end', values=(transaction[1], transaction[2], transaction[3], transaction[4]))