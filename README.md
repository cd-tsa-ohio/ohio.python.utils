# ohio.python.utils
Small utility library to read XLSX or CSV files from a user selected fodler and create data frame for them for data science. Uses a simple filedialog functionality to prompt users to select a folder and one or more files from that folder. Default folder and file types can be customized (see below for Environment variables).

## installation
git clone https://github.com/cd-tsa-ohio/ohio.python.utils.git

cd ohio.python.utils

pip install -e .

## List of functions

getFolderFile - returns chosen folder and teh fiel selected from that folder as strings

getFile - returns a selected single file with its absolute path as string

getFolderFiles

getFiles - returns a list of selected files with their absolute paths as string

getDataFrameFromFile (file) 

getDataFrames

getDataFrame

getFolderFilesDataFrames

getFilesDataFrames

## Environment variables

this utility supports .env file in which the following variables can be defined 

DATA_FOLDER - default is the current folde rin whci teh application runs

SELECTION_MODE - with possihel values 'single' and 'multiple' to allow te user to control mode of the file selection, default value is 'single'

FILE_TYPES - a tuple of file  names and their extensions

'filetypes_0 = (
            ("Excel files", "*.xlsx"), 
            ("Text files", "*.txt"),
            ("CSV files", "*.csv"),
            ("All files", "*.*")
        )'
