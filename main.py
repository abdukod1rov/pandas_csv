import pandas as pd
import hashlib

"""
create a login page with a username and password
create a function that will check the username and password
"""
# user dataframe
users_df = pd.read_csv('Users.csv')

# grades info dataframe
grades_df = pd.read_csv('Students_grade.csv')


# Function for signing up
def signup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Hash the password for security
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    # create a  new DataFrame with the data you want to append
    new_user = pd.DataFrame(
        {'ID': [username.lower()], 'PSW': [hashed_password]}
    )
    # append the new dataframe to th existing one
    new_user_added_df = users_df.append(new_user, ignore_index=True)

    # write the new_user DataFrame back to the existing csv file
    new_user_added_df.to_csv('Users.csv', index=False)


# Function for logging in
def login():
    validUsername = False
    validPassword = False
    global isAdmin
    global isStudent

    isStudent = False
    isAdmin = False

    user_id = ''
    username = input("Enter your username: ").lower()
    password = input("Enter your password: ")
    # hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    for index, row in users_df.iterrows():
        if row['ID'] == username and row['PSW'] == hashed_password:
            validUsername = True
            validPassword = True
            user_id = row['ID']

    if validUsername and validPassword:
        print('Log In Successful')
        if username == 'ad001' or username == 'ad002':
            isAdmin = True
            return user_id
        else:
            isStudent = True
            return user_id

    else:
        print("Invalid Username or Password")
        login()


# deletes a student from the database
def deleteStudentRecord(name, surname):
    studentPresent = False
    # student info dataframe
    global studentInfo_df
    studentInfo_df = pd.read_csv('Student_info.csv')

    for index, row in studentInfo_df.iterrows():
        if row['Name'] == name and row['Surname'] == surname:
            studentPresent = True
    if studentPresent:
        studentInfo_df = studentInfo_df.drop(
            studentInfo_df.loc[(studentInfo_df['Name'] == name) & (studentInfo_df['Surname'] == surname)].index)
    else:
        print('No student available with these credentials')
        deleteStudentRecord(name, surname)
    # studentGrade_df = studentGrade_df.drop(studentGrade_df.loc[(studentGrade_df['ID'] == ID)].index)
    studentInfo_df.to_csv('Student_info.csv', index=False)
    print('Student deleted Successfully')


def changeGrade(ID, subject, grade):
    """Admin enter the student_id, the subject and which grade they want to change
    So, the function takes those parameters and use them as arguments here to perform the function
    """
    studentAvailable = False
    studentGrades_df = pd.read_csv('Students_grade.csv')
    for index, row in studentGrades_df.iterrows():
        if row['ID'] == ID:
            studentAvailable = True
    if studentAvailable:
        studentGrades_df.loc[studentGrades_df['ID'] == ID, subject] = grade
    else:
        print('Make sure to enter valid student id')
        return
    # change back to csv file
    studentGrades_df.to_csv('Students_grade.csv', index=False)
    print('Grade changed successfully!')


def changePayment(ID, status):
    studentAvailable = False
    student = ''
    info_df = pd.read_csv('Student_info.csv')
    # check if the student is present
    for index, row in info_df.iterrows():
        if row['ID'] == ID:
            studentAvailable = True
            student = f'{row["Name"]} {row["Surname"]}'

    if studentAvailable:
        info_df.loc[info_df['ID'] == ID, 'payment_status'] = status
        print(f'Status changed successfully to "{status}" for {student}')

    else:
        print('Invalid student ID')
        return

    info_df.to_csv('Student_info.csv', index=False)


def showStudentsGrade(choice):
    """The 'mean()' method is used to compute the average of the four columns, and the
     resulting series is stored inside the variable  'avg_cols'. The 'axis=1' :argument specifies the
     mean should be computed across columns"""

    info_df = pd.read_csv('Student_info.csv')
    grade_df = pd.read_csv('Students_grade.csv')

    # calculate the average
    avg_cols = grade_df[['Math', 'Programming', 'DataBase', 'English']].mean(axis=1)

    new_fail_df = grade_df.loc[avg_cols < 55]
    # create dataframe where average is above 57
    new_pass_df = grade_df.loc[avg_cols > 57]

    # join failed students with info  table
    failed_students = pd.merge(info_df, new_fail_df, on='ID')

    # join passed students with info table
    passed_students = pd.merge(info_df, new_pass_df, on='ID')
    if choice == 'fail':
        print(failed_students)
    elif choice == 'pass':
        print(passed_students)
    else:
        print("Please enter either 'fail' or 'pass': ")


def showStudentInfo(ID):
    """The main functionality comes from login page. When logged in, the login function returns the userId
    and save that id in our main function. This will prevent from asking the user to enter their id again!
    """
    info_df = pd.read_csv('Student_info.csv')
    grade_df = pd.read_csv('Students_grade.csv')
    # Join the two dataframes on ID

    merged_df = pd.merge(info_df, grade_df, on='ID')
    # Get one row using condition
    getRow = merged_df[merged_df['ID'] == ID]
    print(getRow)


# main function to run the program
def main():
    while True:
        # Prompt the user to choose between sign up and login
        choice = input('Enter 1 to sign up, 2 to log in, and 3 to exit: ')
        if choice == '1':
            signup()
        elif choice == '2':
            id1 = login()
            if isAdmin:
                print('You are the admin! with the id', id1)
                todo = input(
                    'Enter 1 to delete a student record, 2 to change the grade,'
                    ' 3 to change payment status, 4 to see students grades: ')
                if todo == '1':
                    name = input('Enter the student\'s name: ')
                    surname = input('Enter the student\'s surname: ')
                    deleteStudentRecord(name, surname)

                elif todo == '2':
                    student_id = input('Enter the student id: ')
                    subject = input('Which subject would you like to change?: ')
                    grade = input(f'Please, input a new grade for the chosen {subject} subject: ')
                    changeGrade(student_id, subject, grade)
                elif todo == '3':
                    student_id = input('Enter the student ID: ')
                    status = input('Input new payment status; paid or not paid: ')
                    changePayment(student_id, status)

                elif todo == '4':
                    choice = input('Please, select the status of desired students; fail or pass: ').lower()
                    showStudentsGrade(choice)
                else:
                    print('Enter valid code: ')
            elif isStudent:
                print('You are a user with the id', id1)
                select = input('Enter 1 to see your student records: ')
                if select == '1':
                    showStudentInfo(id1)
        elif choice == '3':
            print('Program terminated!')
            break
        else:
            print('Invalid choice. Please try again!')


# Run the program

if __name__ == '__main__':
    main()
