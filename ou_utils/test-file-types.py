import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

def open_file():
    file_path = filedialog.askopenfilename(
        initialdir = "/",
        title = "Select file",
        filetypes = (
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        )
    )
    if file_path:
        print("Selected file:", file_path)

open_file()
