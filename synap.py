import pandas as pd
import re
import math

# remove HTML tags from data
def remove_html(df, indicies):
    pattern = r'reeText' 
    html_tags= r'<.*?>'
    for i in [*indicies]:
        if df[i].str.contains(pattern, regex=True).any():
            df[i] = df[i].str.replace(html_tags, '', regex=True)

# read input csv
df = pd.read_csv('./sample_data/sat_synap_test.csv')

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





#sections = df.
#reading_mod1 = 