import pandas as pd
import re
import math
import gspread
from gspread_dataframe import set_with_dataframe


# CONSTANTS

# user sheet constants
NAME_CELL = 'B11'

ENGLISH_START_ROW = 72-1
ENGLISH_TOTAL = 27
MATH_START_ROW = 140-1
MATH_TOTAL = 22

MOD1_COL = "D"
P_MOD1_COL = 3
MOD2_COL = "K"
P_MOD2_COL = 10

MATH_START_ROW = 140-1


# Student Sheet
STUDENT_SHEET = "Student Sheet"

# synap sheet constants
SYNAP_SHEET = "Synap Test Data"


# gspread
gc = gspread.oauth()

# Open a sheet from a spreadsheet in one go
wks = gc.open("REBECCA Synap Digital SAT Final Diagnostic Grading Master")

def test_rowNames():
    r = 2

    for row in range(2,18):
        formula = "='Student Info'!B"+str(r)

        # spot for the name 
        print("student name")
        print('B12')
        print(formula)

        print("\nenglish mod 1")
        q_start = 72

        # english mod 1
        for i in range(2, 28):
            q_str = str(q_start+i-2)
            print('D'+q_str)
            mod1 = "'Synap Test Data'!H"+str(i)
            print(mod1)
            print("/n")

        # english mod 2
        print("\nenglish mod 2")
        for i in range(2, 28):
            q_str = str(q_start+i-2)
            print('D'+q_str)
            mod1 = "'Synap Test Data'!H"+str(i+27)
            print(mod1)

        m_start = 140

        # math mod 1
        print("\nmath mod 1")
        for i in range(2, 34):
            q_str = str(q_start+i-2)
            print('D'+q_str)
            mod1 = "'Synap Test Data'!H"+str(i+55)
            print(mod1)

        # math mod 2
        for i in range(2, 28):
            #start of english mod 1
            mod1 = "'Synap Test Data'!H"+str(i)
            print(mod1)


pdf_ws = wks.worksheet("02")

data = pdf_ws.get_all_values()


df_pdf = pd.DataFrame(data)


# English Mod 1
for i in range(1, 28):
    q_str = str(ENGLISH_START_ROW+i)
    # do not hard code column
    pdf_ws.update_acell(MOD1_COL+q_str, "=HLOOKUP('Student Sheet'!A3,'Synap Test Data'!1:100,"+str(i + 71)+",FALSE)")



# English Mod 2
for i in range(1, 28):
    q_str = str(ENGLISH_START_ROW+i)
    # do not hard code column, or 27
    pdf_ws.update_acell(MOD2_COL+q_str, "=HLOOKUP('Student Sheet'!A3,'Synap Test Data'!1:100,"+str(i+28)+",FALSE)")


# Math 1
for i in range(1, 23):
    q_str = str(MATH_START_ROW+i)
    # do not hard code column
    pdf_ws.update_acell(MOD1_COL+q_str, "=HLOOKUP('Student Sheet'!A3,'Synap Test Data'!1:100,"+str(i+56)+",FALSE)")


# Math 2
for i in range(1, 23):
    q_str = str(MATH_START_ROW+i)
    # do not hard code column
    pdf_ws.update_acell("L"+q_str, "=HLOOKUP('Student Sheet'!A3,'Synap Test Data'!1:100,"+str(i+78)+",FALSE)")

