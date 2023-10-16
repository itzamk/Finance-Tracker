# main.py

import tkinter as tk
import investment_database
from investment_app import InvestmentApp
#from style import setup_style

if __name__ == "__main__":
    investment_database.setup_database()  # Set up the database when the program starts
    root = tk.Tk()
    #setup_style()
    app = InvestmentApp(root)
    app.run()