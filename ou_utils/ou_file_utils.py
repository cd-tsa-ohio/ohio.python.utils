# module to perform various file operations. Currentlyly implements excel and CSV fiel read and
# generation of pandas dataframe from the file 
# If run as main, prompts user to select a file, reads it, makes dataframe, and shows its head
# 
# Author Dusan Sormaz
# Version 1.0.4
# change log
# Date          Version Author      Content
# 11/22/2024    1.0.1   D. Sormaz   Initial implementation
# 11/27/2024    1.0.2   D. Sormaz   Added multiple file selection options
# 12/24/2024    1.0.3   D. Sormaz   Read file types from .env file
# 01/12/2025    1.0.4   D. Sormaz   Implemented getFilesDataFrames, whci returns a dictionary with 
#                                   files as key and data frames as values
# 01/18/2025    1.0.5   D. Sormaz   fixed the bug in line 77, call to getDataFrameFromFile()
# 01/21/2025    1.0.6   D. Sormaz   simplified default values, lines 30 - ...
# 10/28/2025    1.0.7   D. Sormaz   Added basic error checking if user presses cancel button
# 10/28/2025    1.0.8   D. Sormaz   Added functionality to return the user selected folder where files are opened
#                                   Previous functions are kept for backward compatibility
#                                   functions added: getFolderFile, getFolderFiles, getFolderFilesDataFrames

from decouple import config
from ast import literal_eval as make_tuple
from pathlib import Path
import pandas as pd
import tkinter as tk
from tkinter import filedialog
# code to handle file types
# need to generalize it
filetypes_0 = (
            ("Excel files", "*.xlsx"), 
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        )

DATA_FOLDER = config('DATA_FOLDER', default = '.')
SELECTION_MODE = config('SELECTION_MODE', default = 'single')
try:
    filetypes = make_tuple(config('FILE_TYPES'))
except:
    filetypes = filetypes_0

def getFolderFile():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title='Select one file', initialdir=DATA_FOLDER, filetypes = filetypes)
    if file_path == '':
        raise RuntimeError("User did not make a selection of a single file. Cannot proceed")
    return Path(file_path).parent, file_path

def getFile():
    _, file = getFolderFile ()
    return file

def getFolderFiles():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilenames(title='Select one or more files',initialdir=DATA_FOLDER, filetypes = filetypes)
    if file_path == '':
        raise RuntimeError("User did not make a selection of multiple files. Cannot proceed")
    return Path(file_path[0]).parent, file_path

def getFiles():
    _, files = getFolderFiles()
    return files

def getDataFrameFromFile(file):
    if file.endswith('xlsx'):
        df = pd.read_excel(file)
    elif file.endswith('csv'):
        df = pd.read_csv(file)
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

def getFolderFilesDataFrames():
    folder, files = getFolderFiles()
    files_dataframes = {}
    for f in files:
        df = getDataFrameFromFile(f)
        files_dataframes[f] = df
    return folder, files_dataframes

def getFilesDataFrames ():
    _, files_dataframes = getFolderFilesDataFrames ()
    return files_dataframes


if __name__ == "__main__":
    print (getFile())
    fo, fi = getFolderFiles()
    print (fo)
    print (fi)
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