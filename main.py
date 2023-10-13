import tkinter as tk
import investment_database
from investment_app import InvestmentApp

if __name__ == "__main__":
    investment_database.setup_database()  # Set up the database when the program starts
    root = tk.Tk()
    app = InvestmentApp(root)
    app.run()