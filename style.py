# style.py

import tkinter as tk
from tkinter import ttk

def setup_style():
    style = ttk.Style()

    # Defining colors to use
    dark_color = '#181818'  # Dark background color similar to Twitch's dark mode
    light_color = '#E0E0E0'  # Light text color for contrast against dark background

    # Configure global styles
    style.configure('.', background=dark_color, foreground=light_color)

    # Button styling
    style.configure('TButton',
                    background='gray',
                    foreground='black',
                    font=('Arial', 12, 'bold'),
                    borderwidth=2,
                    focusthickness=3,
                    focuscolor=style.configure(".")["background"])
    style.map('TButton',
              background=[('active', '#6441A4')],  # Change background color when button is active (clicked)
              bordercolor=[('active', light_color)])  # Change border color when button is active (clicked)

    # Label styling
    style.configure('TLabel', background=dark_color, foreground=light_color, font=('Arial', 12))

    # Frame styling
    style.configure('TFrame', background=dark_color)

    # Treeview (Table) styling
    style.configure('Treeview', background=dark_color, foreground=light_color, fieldbackground=dark_color)
    style.map('Treeview', background=[('selected', '#6441A4')])  # Change background color when a row is selected