# main.py

import tkinter as tk
from ttkthemes import ThemedTk
import investment_database
from investment_app import InvestmentApp
import matplotlib.pyplot as plt

if __name__ == "__main__":
    investment_database.setup_database()  # Set up the database when the program starts
    plt.style.use('classic')
    root = ThemedTk(theme='adapta') #plastik?
    app = InvestmentApp(root)
    
    app.run()