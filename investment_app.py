import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from add_asset_window import AddAssetWindow
from inspect_asset_window import InspectAssetWindow
import sqlite3

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        root.title("Investment Tracker")

        self.create_widgets()
        self.update_assets()


    def create_widgets(self):

        # Create table
        self.tree = ttk.Treeview(self.root, columns=('Name', 'Amount', 'Price', 'Value'), show='headings')
        self.tree.heading('Name', text='Investment Name')
        self.tree.heading('Amount', text='Amount Holding')
        self.tree.heading('Price', text='Current Price')
        self.tree.heading('Value', text='Total Value')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame for the pie chart
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create a label for the total value
        self.total_value_label = tk.Label(self.root, text="", font=("Arial", 24, "bold"))
        self.total_value_label.pack(before=self.chart_frame)

        # Create a pie chart
        self.fig, self.ax = plt.subplots()
        sizes = [15, 30, 45, 10] # Dummy data for the pie chart
        labels = ['Asset A', 'Asset B', 'Asset C', 'Asset D']
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Embed the pie chart in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("TButton",
                        font=('Arial', 12),
                        foreground='black',
                        background='black',
                        padding=10,
                        relief=tk.RAISED,
                        width=20)

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)  # Adding some padding around the button frame

        # Apply the style to the buttons and place them in the button frame
        self.add_button = ttk.Button(self.button_frame, text="Add Asset", command=self.open_add_asset_window, style="TButton")
        self.add_button.grid(row=0, column=1, padx=5)  # Adding some padding between the buttons

        self.inspect_button = ttk.Button(self.button_frame, text="Inspect Asset", command=self.open_inspect_asset_window, style="TButton")
        self.inspect_button.grid(row=0, column=0, padx=5)  # Adding some padding between the buttons

        # self.inspect_button = ttk.Button(self.button_frame, text="Remove Asset", command=self.open_inspect_asset_window, style="TButton")
        # self.inspect_button.grid(row=0, column=2, padx=5)  # Adding some padding between the buttons

    def open_add_asset_window(self):
        AddAssetWindow(self.root, self)

    def open_inspect_asset_window(self):
        selected_item = self.tree.selection()
        if selected_item:
            asset_name = self.tree.item(selected_item, 'values')[0]
            InspectAssetWindow(self.root, asset_name)
        else:
            tk.messagebox.showwarning("No Selection", "No asset selected. Please select an asset to inspect.")

    def update_total_value(self):
        total_value = self.get_total_value()
        self.total_value_label.config(text=f"Portfolio Total: ${total_value:,.2f}")

    def update_assets(self):
        # Clear existing rows in the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get updated asset data from the database
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        c.execute('SELECT name, amount, current_price FROM investments')
        assets = c.fetchall()
        conn.close()

        # Insert updated asset data into the table
        for asset in assets:
            asset_name, amount, current_price = asset
            total_value = amount * current_price if current_price is not None else None
            self.tree.insert('', 'end', values=(asset_name, amount, current_price, total_value))

        self.update_total_value()

    def get_total_value(self):
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        total_value = c.execute('SELECT SUM(amount * current_price) FROM investments').fetchone()[0]
        conn.close()
        return total_value

    def run(self):
        self.root.mainloop()