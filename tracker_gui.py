import tkinter as tk
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import investment_database

class InvestmentApp:
    def __init__(self, root):
        self.root = root
        root.title("Investment Tracker")

        self.create_widgets()

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
        self.add_button.grid(row=0, column=0, padx=5)  # Adding some padding between the buttons

        self.inspect_button = ttk.Button(self.button_frame, text="Inspect Asset", command=self.open_inspect_asset_window, style="TButton")
        self.inspect_button.grid(row=0, column=1, padx=5)  # Adding some padding between the buttons

    def open_add_asset_window(self):
        AddAssetWindow(self.root)

    def open_inspect_asset_window(self):
        selected_item = self.tree.selection()
        if selected_item:
            asset_name = self.tree.item(selected_item, 'values')[0]
            InspectAssetWindow(self.root, asset_name)
        else:
            tk.messagebox.showwarning("No Selection", "No asset selected. Please select an asset to inspect.")

    def run(self):
        self.root.mainloop()


class AddAssetWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Asset")

        self.name_label = tk.Label(self, text="Asset Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1)

        self.add_button = tk.Button(self, text="Add Asset", command=self.add_asset)
        self.add_button.grid(row=1, columnspan=2)

    def add_asset(self):
        asset_name = self.name_entry.get()
        if asset_name:
            add_new_asset(asset_name)  # Assume this is a function to add the asset to the database
            self.master.update_assets()  # Update the main window to reflect the new asset
            self.destroy()  # Close the AddAssetWindow

class InspectAssetWindow(tk.Toplevel):
    def __init__(self, master, asset_name):
        super().__init__(master)
        self.title(f"Inspecting {asset_name}")

        asset_details, transaction_history = get_asset_details(asset_name)

if __name__ == "__main__":
    investment_database.setup_database()  # Set up the database when the program starts
    root = tk.Tk()
    app = InvestmentApp(root)
    app.run()