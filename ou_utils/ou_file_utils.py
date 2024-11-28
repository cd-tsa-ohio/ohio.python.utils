# module to perform various file operations. Currentlyly implements excel and CSV fiel read and
# generation of pandas dataframe from the file 
# If run as main, prompts user to select a file, reads it, makes dataframe, and shows its head
# 
# Author Dusan Sormaz
# Version 1.0.1 
# change log
# Date          Author      Content
# 11/22/2024    D. Sormaz   Intial implementation
# 11/27/2024    D. Sormaz   Added multiple file selection options
from decouple import config
import pandas as pd
import tkinter as tk
from tkinter import filedialog
# code to handle file types
# need to generalize it
filetypes = (
            ("Excel files", "*.xlsx"), 
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        )

try: 
    DATA_FOLDER = config('DATA_FOLDER')
except:
    DATA_FOLDER = '.'
try:
    SELECTION_MODE = config('SELECTION_MODE')
except:
    SELECTION_MODE = 'single'

def getFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Select one file', initialdir=DATA_FOLDER, filetypes = filetypes)
    return file_path

def getFiles():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames(title='Select one or more files',initialdir=DATA_FOLDER, filetypes = filetypes)
    return file_path

def getDataFrameFromFile(file):
    if file.endswith('xlsx'):
        df = pd.read_excel(file)
    elif file.endswith('csv'):
        df = pd.reads_csv(file)
    else:
        ext = file[file.rindex('.'):]
        raise NotImplementedError (f'Not supported file extension: {ext}')
    return df

def getDataFrames():
    df_list = []
    f_list = getFiles()
    for file in f_list:
        df_list.append(getDataFrameFromFile(file))
    return df_list

def getDataFrame():
        return getDataFrameFromFile(getFile())

if __name__ == "__main__":
    if SELECTION_MODE.lower() == 'single':
        df = getDataFrame()
        print(df.head())
    elif SELECTION_MODE.lower() == 'multiple':
        f_list = getFiles()
        print(f_list)
        df = getDataFrameFromFile(f_list[0])
        print(df.head())
else:
    print(f'Incorrect selection mode env variable: {SELECTION_MODE}')