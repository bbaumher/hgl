import pandas as pd
import re
import math
import gspread
from gspread_dataframe import set_with_dataframe
import time
from enum import Enum

class TestType(Enum):
    SAT_Init = "SAT Initial"
    SAT_Final = "SAT Final"
    ACT_Init = "ACT Initial"
    ACT_Final = "ACT Final"


SAT_FINAL_CSV = './sample_data/sat_synap_test.csv'


DEFAULT_CSV = './sample_data/Synap_SAT_1.csv'
DEFAULT_OUTPUT = "Synap Digital SAT TEST"

SAT_INIT_TEMPLATE = "REBECCA Synap Digital SAT Initial Diagnostic Grading Master"
#SAT_INIT_TEMPLATE = "TEST REBECCA Synap Digital SAT Initial Diagnostic Grading Master (Kelsie)", "TEST TEST"
SAT_FINAL_TEMPLATE = "REBECCA Synap Digital SAT Final Diagnostic Grading Master"
ACT_INIT_TEMPLATE = "REBECCA Synap ACT Initial Diagnostic Grading Master"
ACT_FINAL_TEMPLATE = "REBECCA Synap Digital ACT Final Diagnostic Grading Master"

# probably dont need. think its SAT initial 
DEFAULT_TEMPLATE_ID = "1JPF-sU0gauEhh13608ZIEcbgww1yUinmY1CKcuHwjoM"

def GetTemplateName(test):
    if test == TestType.SAT_Init:
        return SAT_INIT_TEMPLATE
    elif test == TestType.SAT_Final:
        return SAT_FINAL_TEMPLATE
    elif test == TestType.ACT_Init:
        return ACT_INIT_TEMPLATE
    elif test == TestType.ACT_Final:
        return ACT_FINAL_TEMPLATE
    else:
        # Handle this else where?
        return None


# remove HTML tags from data
def remove_html(df, indicies):
        pattern = r'reeText' 
        html_tags= r'<.*?>'
        for i in [*indicies]:
            if df[i].str.contains(pattern, regex=True).any():
                df[i] = df[i].str.replace(html_tags, '', regex=True)

def filter_non_digits(string: str) -> str:
    result = ''
    for char in string:
        if char in '-1234567890./':
            result += char
    return result 


def printTimeElapsed(t0):
    print("TIME: " + str(time.time()-t0))

def ProcessSynapData(csv_file, output_sht, template):
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

    # Get template name for selected test
    temp = GetTemplateName(template)

    # gspread
    gc = gspread.oauth()
    template = gc.open(temp)

    
    gc.copy(template.id, title=output_sht)

    # Open new sheet that is a copy
    wks = gc.open(output_sht)
    wks.share("rebecca@highergroundlearning.com", perm_type='user', role='writer')

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % wks.id


  
    # Create new sheets if they do not exist, student sheet and synap sheet
    try:
        student_ws = wks.worksheet(STUDENT_SHEET)
    except gspread.exceptions.WorksheetNotFound:
        student_ws = wks.add_worksheet(title=STUDENT_SHEET, rows=100, cols=20)

    try:
        test_data_ws = wks.worksheet(SYNAP_SHEET)
    except gspread.exceptions.WorksheetNotFound:
        test_data_ws = wks.add_worksheet(title=SYNAP_SHEET, rows=100, cols=20)


    # read input csv
    # TODO: Add try / catch
    df = pd.read_csv(csv_file)

    # get various columns and rows, as stated
    columns = df.columns.to_list()
    first_row = df.iloc[0]
    first_student_idx = df[columns[0]].first_valid_index();

    # get user info columns that we want
    r = re.compile('User .*|Time.*')
    user_columns = list(filter(r.match, columns)) 
    df_user_cols = df.filter(user_columns)

    # df with only student rows
    df_students = df_user_cols.iloc[first_student_idx:]

    # test data starts where first row has values
    test_begin = first_row.first_valid_index()
    test_idx = [i for i, item in enumerate(columns) if re.search(test_begin, item)][0]
    question_columns = columns[test_idx:]

    # remove HTML tags from free response
    remove_html(df, question_columns)
    free_response = df.columns[df.isin(['input:freeText']).any()] 

    for col in free_response:
        frame = df[col]
        for i in range(first_student_idx, df.shape[0]):
            str = frame[i]
            try:
                temp = filter_non_digits(frame[i])
            except :
                temp = ""
                str = ""
            frame[i] = temp
            str += " -> " + temp
            print(str)
            


    # now get only test questions, with student ID
    df_test_info = df
    df_test_info.loc[df_students.index,test_begin] = df_students[columns[0]]

    df_test_info = df_test_info.filter([*question_columns])
    df_transposed = df_test_info.T

    # reset column names
    new_header = df_transposed.iloc[0] 
    df_transposed = df_transposed[1:] 
    df_transposed.columns = new_header

    # output only test questions with student IDS
    df_transposed.to_csv('sample_test.csv', index=False)

    # output table of just student info
    df_students.to_csv('sample_students.csv', index=False)


    # only write if not already written?
    set_with_dataframe(student_ws, df_students)
    set_with_dataframe(test_data_ws, df_transposed)

    return spreadsheet_url



if __name__ == "__main__":
    ProcessSynapData(DEFAULT_CSV, "TEST TEST init",TestType.SAT_Init) 