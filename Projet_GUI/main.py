# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 12:17:31 2025
@author: aaitb
"""
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from gui import guiMenu  
import os
import sys


# Helper function to get the resource path (for PyInstaller compatibility)
def resource_path(relative_path):
    """ Get the absolute path to a resource. Works for PyInstaller. """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Create the main Tkinter window
main = tk.Tk()
main.title("La recherche operationnel")
main.geometry("1000x800")  # Increased window size for better proportions
main.configure(bg="#303030")  # Dark background
main.resizable(False, False)  # Fix window size

# Apply Calibri font
calibri_font = ("Calibri", 14)
title_font = ("Calibri", 32, "bold")
subtitle_font = ("Calibri", 12)
info_font = ("Calibri", 12, "italic")

# Define styles for ttk buttons
style = ttk.Style()
style.theme_use("clam")

# Configure button style
style.configure(
    "Custom.TButton",
    background="#3F51B5",
    foreground="white",
    font=calibri_font,
    padding=(30, 15),  # Wider buttons
    borderwidth=0,
    borderradius=20,
)

style.map(
    "Custom.TButton",
    background=[("active", "#5C6BC0")],
    foreground=[("active", "white")],
)

# Create a main container frame
container = tk.Frame(main, bg="#303030")
container.pack(expand=True, fill="both", padx=40, pady=40)

# Create a title frame
title_frame = tk.Frame(container, bg="#303030")
title_frame.pack(fill="x", pady=(0, 30))

# Main title with enhanced styling
title_label = tk.Label(
    title_frame,
    text="La Recherche Operationnel",
    font=title_font,
    bg="#303030",
    fg="#F0F8FF",
)
title_label.pack(pady=(0, 10))

# Add a subtitle
subtitle_label = tk.Label(
    title_frame,
    text="System d'optimisation et aide à la décision",
    font=subtitle_font,
    bg="#303030",
    fg="#AAAAAA",  # Lighter gray for subtitle
)
subtitle_label.pack()

# Add the photo section
photo_frame = tk.Frame(container, bg="#303030")
photo_frame.pack(pady=(0, 30))

# Load the photo dynamically
image_path = resource_path("emsi.png")  # Get the correct path to the image
photo = PhotoImage(file=image_path)
photo_label = tk.Label(photo_frame, image=photo, bg="#303030")
photo_label.pack()

info_label = tk.Label(
    container,
    text="Réalisé par Ait ben moumen Adam\nSous l'encadrement de Dr. El Mkhalet Mouna",
    font=info_font,
    bg="#303030",
    fg="#F0F8FF"
)
info_label.pack(pady=(20, 10))

# Create a decorative line
separator = ttk.Separator(container, orient="horizontal")
separator.pack(fill="x", pady=(0, 30))

# Create a frame for buttons with better spacing
button_frame = tk.Frame(container, bg="#303030")
button_frame.pack(pady=20)

# Create styled buttons with more space between them
enter_button = ttk.Button(
    button_frame,
    text="Commencer",  # More descriptive text
    style="Custom.TButton",
    command=guiMenu
)
enter_button.pack(side=tk.LEFT, padx=20)

close_button = ttk.Button(
    button_frame,
    text="Quitter",  # More descriptive text
    style="Custom.TButton",
    command=main.destroy
)
close_button.pack(side=tk.LEFT, padx=20)

# Add a footer with version info
footer_label = tk.Label(
    container,
    text="Version 1.0",
    font=("Calibri", 10),
    bg="#303030",
    fg="#666666"
)
footer_label.pack(side="bottom", pady=20)

# Center the window on the screen
window_width = 800
window_height = 600
screen_width = main.winfo_screenwidth()
screen_height = main.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
main.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Start the Tkinter event loop
main.mainloop()
