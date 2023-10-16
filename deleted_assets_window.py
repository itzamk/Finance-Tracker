import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from investment_database import restore_asset

class DeletedAssetsWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.title("Deleted Assets")

        self.create_widgets()

    def create_widgets(self):
        self.tree = ttk.Treeview(self, columns=('Name', 'Amount', 'Price', 'Value'), show='headings')
        self.tree.heading('Name', text='Investment Name')
        self.tree.heading('Amount', text='Amount Holding')
        self.tree.heading('Price', text='Current Price')
        self.tree.heading('Value', text='Total Value')
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill="x")  # Filling along the x-axis to take full width

        self.restore_button = ttk.Button(self.button_frame, text="Restore Asset", command=self.restore_selected_asset)
        self.restore_button.pack(pady=5)  # Adding some padding around the button

        self.update_deleted_assets()

    def restore_selected_asset(self):
        selected_item = self.tree.selection()
        if selected_item:
            asset_name = self.tree.item(selected_item, 'values')[0]
            restore_asset(asset_name)
            self.update_deleted_assets()
            self.app.update_assets()
        else:
            tk.messagebox.showwarning("No Selection", "No asset selected. Please select an asset to restore.", parent=self)

    def update_deleted_assets(self):
        for row in self.tree.get_children():
            self.tree.delete(row)  # Clear existing rows in the table

        conn = sqlite3.connect('investments.db')
        c = conn.cursor()
        c.execute('SELECT name, amount, current_price FROM investments WHERE deleted = 1')
        deleted_assets = c.fetchall()
        conn.close()

        for asset in deleted_assets:
            asset_name, amount, current_price = asset
            total_value = amount * current_price if current_price is not None else None
            self.tree.insert('', 'end', values=(asset_name, amount, current_price, total_value))