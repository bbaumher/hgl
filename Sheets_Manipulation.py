import pandas as pd
import re
import math
import gspread
from gspread_dataframe import set_with_dataframe
import time
import bisect 

DEFAULT_CSV = './sample_data/Synap_SAT_1.csv'
DEFAULT_OUTPUT = "Synap Digital SAT TEST"

DEFAULT_TEMPLATE = "REBECCA Synap Digital SAT Initial Diagnostic Grading Master"
DEFAULT_FINAL_TEMPLATE = "REBECCA Synap Digital SAT Final Diagnostic Grading Master"
DEFAULT_ACT_TEMPLATE = "REBECCA Synap ACT Initial Diagnostic Grading Master"

DEFAULT_TEMPLATE_ID = "1JPF-sU0gauEhh13608ZIEcbgww1yUinmY1CKcuHwjoM"
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

# ACT Constants
ACT_ENG_TOT = 75
ACT_MATH_TOT = 60
ACT_READING_TOT = 40
ACT_SCI_TOT = 40

# Student Sheet
STUDENT_SHEET = "Student Sheet"

# synap sheet constants
SYNAP_SHEET = "Synap Test Data"

def AuthorizeAndOpen():
    gc = gspread.oauth()
    return gc

def NumToSheetName(wks_num):
    if wks_num < 10:
        return "0"+str(wks_num)
    else:
        return str(wks_num)

def AddNameCell(ws, idx):
    print(str(idx))
    ws.update_acell(NAME_CELL, "=\'"+STUDENT_SHEET+"\'!B"+str(idx))

def SleepIfRequestLimit(total_writes, sleep_time = 30):
    if total_writes % 60 == 0:
        time.sleep(sleep_time)
        print("sleeping for request limit")


def AddHLookup(ws, idx,
                  student_sheet=STUDENT_SHEET, 
                    synap_sheet=SYNAP_SHEET, 
                    mod1_col=MOD1_COL,
                    mod2_col=MOD2_COL,
                    eng_start=ENGLISH_START_ROW,
                    math_start=MATH_START_ROW):
    # English Mod 1
    for i in range(1, 28):
        q_str = str(eng_start+i)
        # do not hard code column
        ws.update_acell(mod1_col+q_str, "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+",\'"+synap_sheet+"\'!1:100,"+str(i + 1)+",FALSE)")


    # English Mod 2
    for i in range(1, 28):
        q_str = str(eng_start+i)
        # do not hard code column, or 27
        ws.update_acell(mod2_col+q_str, "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+",\'"+synap_sheet+"\'!1:100,"+str(i+28)+",FALSE)")
    
    time.sleep(60)

    # Math 1
    for i in range(1, 23):
        q_str = str(math_start+i)
        # do not hard code column
        ws.update_acell(mod1_col+q_str, "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+",\'"+synap_sheet+"\'!1:100,"+str(i+56)+",FALSE)")


    # Math 2
    for i in range(1, 23):
        q_str = str(math_start+i)
        # do not hard code column
        ws.update_acell("L"+q_str, "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+",\'"+synap_sheet+"\'!1:100,"+str(i+78)+",FALSE)")

    time.sleep(60)

def AddHLookupACT(ws, idx, total_writes,
                  student_sheet=STUDENT_SHEET, 
                    synap_sheet=SYNAP_SHEET, 
                    mod1_col=MOD1_COL,
                    mod2_col=MOD2_COL,
                    eng_start=180-1,
                    math_start=238-1):
    print("\n\n\nstarting " + ws.title)
    print("total requests " + str(total_writes))
    # TODO(no hard code)
    mod1_col = "C"
    
    # English
    print("starting english")
    for i in range(1, ACT_ENG_TOT + 1):
        q_str = str(eng_start+i)
        # do not hard code column
        ws.update_acell(mod1_col+q_str, 
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+str(i + 1)+",FALSE)")
        total_writes +=1
        if i == 40:
            mod1_col="L"
            eng_start = eng_start-40
        SleepIfRequestLimit(total_writes)

    mod1_col = "C"

    #  Math
    print("starting math")
    for i in range(1, ACT_MATH_TOT + 1):
        q_str = str(math_start+i)
        # do not hard code column, or 27
        ws.update_acell(mod1_col+q_str, 
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+str(i+ACT_ENG_TOT+1)+",FALSE)")
        if i == 30:
            mod1_col="L"
            math_start = math_start-30
        total_writes +=1
        SleepIfRequestLimit(total_writes)

    
    mod1_col = "C"

    # READING
    print("starting reading")
    for i in range(1, ACT_READING_TOT + 1):
        q_str = str(295+i)
        # do not hard code column
        ws.update_acell(mod1_col+q_str, 
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+str(i+ACT_ENG_TOT+ACT_MATH_TOT+2)+",FALSE)")
        total_writes +=1
        SleepIfRequestLimit(total_writes)


    # SCIENCE
    print("starting science")
    for i in range(1, ACT_SCI_TOT + 1):
        q_str = str(295+i)
        # do not hard code column
        ws.update_acell("L"+q_str, 
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+
                        str(i + ACT_ENG_TOT + ACT_MATH_TOT + ACT_READING_TOT + 2)+",FALSE)")
        total_writes +=1
        SleepIfRequestLimit(total_writes)
    return total_writes

def AddFormula(ws, idx, requests ):
    if requests % 60 == 0:
        time.sleep(50)
        print("sleeping!")
    ws.update_acell("E147", "=IF(isNumber(D147), if(ABS(value(D147)-0.2)<0.01,1,0), IF(D147=\"1/5\",1,0))")
    requests += 1
    ws.update_acell("E155", "=IF(isNumber(D155), if(ABS(value(D155)-361/8)<0.01,1,0), IF(D155=\"361/8\",1,0))")
    requests += 1
    ws.update_acell("M141", "=IF(OR(L141=15, L141=-5),1,0)")
    requests += 1
    ws.update_acell("M147", "=IF(isNumber(L147), if(ABS(value(L147)-3/10)=0,1,0), IF(L147=\"3/10\",1,0))")
    requests += 1
    ws.update_acell("M154", "=IF(isNumber(L154), if(ABS(value(L154)-15/17)<0.01,1,0), IF(L154=\"15/17\",1,0))")
    requests += 1 

    return requests 


def AddHLookupFake(ws, idx, total_writes,
                  student_sheet=STUDENT_SHEET, 
                    synap_sheet=SYNAP_SHEET, 
                    mod1_col=MOD1_COL,
                    mod2_col=MOD2_COL,
                    eng_start=180-1,
                    math_start=238-1):
    print("\n\n\nstarting " + ws.title)
    print("total requests " + str(total_writes))
    # TODO(no hard code)
    mod1_col = "C"
    
    # English
    print("starting english")
    for i in range(1, ACT_ENG_TOT + 1):
        q_str = str(eng_start+i)
        # do not hard code column
        """print("updating: " + mod1_col+q_str + ": to " +
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+str(i + 1)+",FALSE)")
        """
        total_writes +=1
        if i == 40:
            mod1_col="L"
            eng_start = eng_start-40
        SleepIfRequestLimit(total_writes,1)

    mod1_col = "C"

    #  Math
    print("starting math")
    for i in range(1, ACT_MATH_TOT + 1):
        q_str = str(math_start+i)
        # do not hard code column, or 27
        """print("updating " + mod1_col+q_str + "to : " +
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+str(i+ACT_ENG_TOT+1)+",FALSE)")
        """
        if i == 30:
            mod1_col="L"
            math_start = math_start-30
        total_writes +=1
        SleepIfRequestLimit(total_writes,1)

    
    mod1_col = "C"

    # READING
    print("starting reading")
    for i in range(1, ACT_READING_TOT + 1):
        q_str = str(295+i)
        # do not hard code column
        """        print("updating " + mod1_col+q_str + " to: " + 
                                "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                                ",\'"+synap_sheet+"\'!1:1000,"+str(i+ACT_ENG_TOT+ACT_MATH_TOT+2)+",FALSE)")
        """
        total_writes +=1
        SleepIfRequestLimit(total_writes,1)


    # SCIENCE
    print("starting science")
    for i in range(1, ACT_SCI_TOT + 1):
        q_str = str(295+i)
        # do not hard code column
        """print("updating " + "L"+q_str + " to: " + 
                        "=HLOOKUP(\'"+student_sheet+"\'!A"+str(idx)+
                        ",\'"+synap_sheet+"\'!1:1000,"+
                        str(i + ACT_ENG_TOT + ACT_MATH_TOT + ACT_READING_TOT + 2)+",FALSE)")
        """
        total_writes +=1
        SleepIfRequestLimit(total_writes,1)
    return total_writes


def UpdateAllSheets(wks, func, 
                    student_sheet=STUDENT_SHEET, 
                    synap_sheet=SYNAP_SHEET, 
                    mod1_col=MOD1_COL,
                    mod2_col=MOD2_COL,
                    eng_start=ENGLISH_START_ROW,
                    math_start=MATH_START_ROW):
    requests=0
    idx=2
    for x in range (1, 25):
        wks_str = NumToSheetName(x)
        try:
            pdf_ws = wks.worksheet(wks_str)
        except gspread.exceptions.WorksheetNotFound:
            pdf_ws = wks.duplicate_sheet(pdf_ws.id, new_sheet_name=wks_str)
        
        temp = func(pdf_ws, idx, requests)
        requests = temp
        idx +=1
        print(wks_str)


def ReOrderTabs(wks):
    total_sheets = wks.worksheets()
    non_pdfs = []
    for ele in total_sheets:
        if len(ele.title) > 2:
            non_pdfs.append(ele)
        else:
            print(ele.title)
            #Nothing
    for i in range(1, 25):
        non_pdfs.append(wks.worksheet(NumToSheetName(i)))
    wks.reorder_worksheets(non_pdfs)

def AnotherIteration(df_students, pdf_ws):
    r = 2
    for index, row in df_students.iterrows():

        # do not hard code B?
        formula = "="+"\'"+STUDENT_SHEET+"\'!B"+str(r)
        pdf_ws.update_acell(NAME_CELL, formula)

        # English Mod 1
        for i in range(1, 28):
            q_str = str(ENGLISH_START_ROW+i-1)
            # do not hard code column
            pdf_ws.update_acell(MOD1_COL+q_str, "=\'"+SYNAP_SHEET+'\'!H'+str(i+1))
            
        # English Mod 2
        for i in range(1, 28):
            q_str = str(ENGLISH_START_ROW+i-1)
            # do not hard code column, or 27
            pdf_ws.update_acell(MOD2_COL+q_str, "=\'"+SYNAP_SHEET+'\'!H'+str(i+28))

        # Math 1
        for i in range(1, 23):
            q_str = str(MATH_START_ROW+i-2)
            # do not hard code column
            pdf_ws.update_acell(MOD1_COL+q_str, "=\'"+SYNAP_SHEET+'\'!H'+str(i+56))
        
        # Math 2
        for i in range(1, 23):
            q_str = str(MATH_START_ROW+i-2)
            # do not hard code column
            pdf_ws.update_acell(MOD2_COL+q_str, '='+SYNAP_SHEET+'!H'+str(i+78))

        r = r+1
        template_sheet = wks.duplicate_sheet(pdf_ws.id, new_sheet_name=str(r))
        
        print(row["User name"])




if __name__ == "__main__":
    gc = AuthorizeAndOpen()
    wks = gc.open("TEST REBECCA Synap Digital SAT Initial Diagnostic Grading Master (Kelsie)")
    ReOrderTabs(wks)
    #UpdateAllSheets(wks, AddFormula)


