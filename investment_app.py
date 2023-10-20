# investment_app.py

import sqlite3
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from add_asset_window import AddAssetWindow
from inspect_asset_window import InspectAssetWindow
from deleted_assets_window import DeletedAssetsWindow
from investment_database import soft_delete_asset, start_auto_refresh

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        root.title("Investment Tracker")

        self.create_widgets()
        self.update_assets()
        self.schedule_refresh()
        start_auto_refresh()

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
        # sizes = [15, 30, 45, 10] # Dummy data for the pie chart
        # labels = ['Asset A', 'Asset B', 'Asset C', 'Asset D']
        # self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        # self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Embed the pie chart in the Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # style = ttk.Style()
        # style.configure("TButton",
        #                 font=('Arial', 12),
        #                 foreground='black',
        #                 background='black',
        #                 padding=10,
        #                 relief=tk.RAISED,
        #                 width=20)

        # Create a frame to hold the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)  # Adding some padding around the button frame

        # Apply the style to the buttons and place them in the button frame
        self.add_button = ttk.Button(self.button_frame, text="Add Asset", command=self.open_add_asset_window, style="TButton")
        self.add_button.grid(row=0, column=1, padx=5)

        self.inspect_button = ttk.Button(self.button_frame, text="Inspect Asset", command=self.open_inspect_asset_window, style="TButton")
        self.inspect_button.grid(row=0, column=0, padx=5)

        self.inspect_button = ttk.Button(self.button_frame, text="Remove Asset", command=self.delete_asset, style="TButton")
        self.inspect_button.grid(row=0, column=2, padx=5)

        self.view_deleted_button = ttk.Button(self.button_frame, text="View Deleted Assets", command=self.open_deleted_assets_window, style="TButton")
        self.view_deleted_button.grid(row=0, column=3, padx=5)

    def update_pie_chart(self):
        # Fetch the data from the database
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()

        c.execute('''
            SELECT name, amount, current_price 
            FROM investments 
            WHERE deleted = 0 AND (amount * current_price) > 0
        ''')

        assets = c.fetchall()
        conn.close()

        # Separate the data into labels and sizes
        labels = [asset[0] for asset in assets]
        sizes = [asset[1] for asset in assets]

        # Clear the existing pie chart
        self.ax.clear()

        # Draw the new pie chart
        self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Draw the canvas again to update the display
        self.canvas.draw()
        
    def open_add_asset_window(self):
        AddAssetWindow(self.root, self)

    def open_inspect_asset_window(self):
        selected_item = self.tree.selection()
        if selected_item:
            asset_id = self.tree.item(selected_item, 'tags')[0]
            InspectAssetWindow(self.root, asset_id, self)
        else:
            tk.messagebox.showwarning("No Selection", "No asset selected. Please select an asset to inspect.")

    def delete_asset(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmation = tk.messagebox.askyesno(
                "Confirm Deletion", 
                "Are you sure you want to delete this asset?"
            )
            if confirmation:
                asset_id = self.tree.item(selected_item, 'tags')[0]
                soft_delete_asset(asset_id)
                self.update_ui()
        else:
            tk.messagebox.showwarning("No Selection", "No asset selected. Please select an asset to remove.")

    def open_deleted_assets_window(self):
        DeletedAssetsWindow(self.root, self)

    def update_total_value(self):
        total_value = self.get_total_value()

        if total_value is None:
            total_value = 0  # Set total_value to 0 if it's None
        self.total_value_label.config(text=f"Portfolio Total: ${total_value:,.2f}")

    def update_assets(self):
        # Clear existing rows in the table
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Get updated asset data from the database
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        c.execute('SELECT id, name, amount, current_price FROM investments WHERE deleted = 0')
        assets = c.fetchall()
        conn.close()

        # Insert updated asset data into the table
        for asset in assets:
            asset_id, asset_name, amount, current_price = asset
            total_value = amount * current_price if amount is not None and current_price is not None else None
            self.tree.insert('', 'end', values=(asset_name, amount, current_price, total_value), tags=(asset_id))

        self.update_total_value()
        self.update_pie_chart()

    def get_total_value(self):
        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        total_value = c.execute('SELECT SUM(amount * current_price) FROM investments').fetchone()[0]
        conn.close()
        return total_value
    
    def update_ui(self):
        self.update_assets()
        self.update_total_value()
    
    def schedule_refresh(self):
        self.update_ui()
        self.root.after(10000, self.schedule_refresh)  # Schedule the next refresh

    def run(self):
        #self.schedule_ui_update()
        self.root.mainloop()
        
    # def schedule_ui_update(self):
    #     self.update_ui()  # Update the UI
    #     self.root.after(10000, self.schedule_ui_update)  # Schedule the next update in 60 seconds (60000 milliseconds)