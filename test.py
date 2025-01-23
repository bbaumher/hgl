import pandas as pd
import re
import math
import gspread
from gspread_dataframe import set_with_dataframe




# gspread
gc = gspread.oauth()

# Open a sheet from a spreadsheet in one go
wks = gc.open("REBECCA Synap Digital SAT Final Diagnostic Grading Master")



# define workbook, etc in def
def del_worksheets():
    for i in range(3,10): 
        temp = "0"+str(i)
        try:
            ws = wks.worksheet(temp)
            wks.del_worksheet(ws)
        except:
            print(temp + " does not exist")

    for i in range(10,25): 
        temp = str(i)
        try:
            ws = wks.worksheet(temp)
            wks.del_worksheet(ws)
        except:
            print(temp + " does not exist")

del_worksheets()

