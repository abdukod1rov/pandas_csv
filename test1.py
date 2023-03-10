# import pandas as pd
#
# # create a sample dataframe
# df = pd.DataFrame({'Col1': [10, 70, 80], 'Col2': [30, 40, 50], 'Col3': [20, 30, 40], 'Col4': [10, 20, 30]})
#
# # create a boolean mask for the rows where the sum is greater than 100
# mask = df.sum(axis=1) > 100
#
# # create a new dataframe with only the rows where the sum is greater than 100
# new_df = df.loc[mask, :]
#
# print(new_df)
import csv


def find_failed_students(subject):
    # Open the students_grade.csv file
    with open('students_grade.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # Create an empty list to store the failed students
        failed_students = []

        # Loop through the records in the file
        for row in reader:
            # Check if the subject matches the input subject and the grade is lower than 60
            if subject in row and row[subject].isdigit() and int(row[subject]) < 60:
                # Add the student's ID and grade for the subject to the list of failed students
                failed_students.append({'ID': row['ID'], subject: row[subject]})

        # Return the list of failed students
        return failed_students


subject = input("Enter subject: ")
failed_students = find_failed_students(subject)

# Print the results
print(f"Students who failed {subject}:")
for student in failed_students:
    print(student)