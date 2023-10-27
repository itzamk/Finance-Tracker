# add_asset_window.py

import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from investment_database import add_new_asset
from coingecko import fetch_assets, fetch_asset_info
import requests

class AddAssetWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.title("Add New Asset")

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        self.search_box = tk.Entry(self)
        self.search_box.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        self.search_box.bind('<KeyRelease>', self.on_search)

        self.tree = ttk.Treeview(self, columns=("Name", "Ticker"), show='headings')
        self.tree.heading("Name", text="Name")
        self.tree.heading("Ticker", text="Ticker")
        self.tree.grid(row=1, column=0, columnspan=2, sticky=tk.NSEW)
        self.tree.bind('<<TreeviewSelect>>', self.on_row_selected)  # Bind the selection event

        self.info_frame = tk.Frame(self)  # Frame for displaying asset information
        self.info_frame.grid(row=1, column=2, sticky=tk.NSEW)

        self.add_button = tk.Button(self, text="Add Asset", command=self.add_asset)
        self.add_button.grid(row=2, columnspan=3)

    def populate_table(self):
        self.assets = fetch_assets()
        if self.assets:
            for asset in self.assets:
                # Store the asset ID as a tag for the item
                self.tree.insert("", tk.END, values=(asset['name'], asset['symbol'].upper()), tags=(asset['id'],))

    def on_search(self, event=None):
        query = self.search_box.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)  # clear the current table contents
        for asset in self.assets:
            if query in asset['name'].lower() or query in asset['symbol'].lower():
                self.tree.insert("", tk.END, values=(asset['name'], asset['symbol'].upper()), tags=(asset['id'],))

    def on_row_selected(self, event):
        selected_items = self.tree.selection()  # get selected items
        if not selected_items:  # Check if the selection is empty
            return  # Exit the method if the selection is empty

        selected_item = selected_items[0]  # get selected item
        asset_id = self.tree.item(selected_item, "tags")[0]  # Get the asset ID tag
        self.display_asset_info(asset_id)

    def display_asset_info(self, asset_id):
        asset_info = fetch_asset_info(asset_id)

        # Clear any existing info
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        # Display the new info
        if asset_info:
            font_bold = tkFont.Font(weight="bold")
            tk.Label(self.info_frame, text=f"Asset Information", font=font_bold).pack(anchor=tk.W)
            tk.Label(self.info_frame, text=f"Name: {asset_info['name']}").pack(anchor=tk.W)
            tk.Label(self.info_frame, text=f"Ticker: {asset_info['ticker']}").pack(anchor=tk.W)
            tk.Label(self.info_frame, text=f"Price: ${asset_info['price']}").pack(anchor=tk.W)
        else:
            tk.Label(self.info_frame, text="No information available").pack(anchor=tk.W)

    def add_asset(self):
        selected_items = self.tree.selection()  # get selected items
        if not selected_items:  # Check if the selection is empty
            return  # Exit the method if the selection is empty

        selected_item = selected_items[0]  # get selected item
        asset_name = self.tree.item(selected_item)["values"][0]
        asset_id = self.tree.item(selected_item)["tags"][0]
        if asset_name and asset_id:
            add_new_asset(asset_id, asset_name)
            self.app.update_assets()  # Update the main window's table
            self.destroy()  # Close the AddAssetWindow after adding the asset