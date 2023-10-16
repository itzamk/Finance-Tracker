# add_asset_window.py

import tkinter as tk
from investment_database import add_new_asset

class AddAssetWindow(tk.Toplevel):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.title("Add New Asset")

        self.name_label = tk.Label(self, text="Asset Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        self.add_button = tk.Button(self, text="Add Asset", command=self.add_asset)
        self.add_button.grid(row=1, columnspan=2)

    def add_asset(self):
        asset_name = self.name_entry.get()
        if asset_name:  # check if the entry is not empty
            add_new_asset(asset_name)
            self.app.update_assets()  # Update the main window's table
            self.destroy()  # Close the AddAssetWindow after adding the asset