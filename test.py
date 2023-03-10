import pandas as pd
import numpy as np

info_df = pd.read_csv('Student_info.csv')
grade_df = pd.read_csv('Students_grade.csv')

avg_cols = grade_df[['Math', 'Programming', 'DataBase', 'English']].mean(axis=1)
new_df = grade_df.loc[avg_cols < 55]
mark4 = grade_df.loc[avg_cols > 57]


passed_df = pd.merge(info_df, mark4, on='ID')
failed_df = pd.merge(info_df, new_df, on='ID')
print(failed_df)
print(passed_df)
# create the first dataframe
df1 = pd.DataFrame({'ID': ['A', 'B', 'C'], 'Value1': [10, 20, 30]})

# create the second dataframe
df2 = pd.DataFrame({'ID': ['B', 'C', 'D'], 'Value2': [40, 50, 60]})

# merge the dataframes on the 'ID' column
merged_df = pd.merge(df1, df2, on='ID')

# # check if the student is present
# for index, row in info_df.iterrows():
#     if row['ID'] == 'st002':
#         info_df.loc[info_df['ID'] == 'st002', 'payment_status'] = 'not paid'
#
#     else:
#         print('Invalid student ID')
#
# # info_df.to_csv('Student_info.csv', index=False)
# print(info_df)
