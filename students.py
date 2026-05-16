import mysql.connector
from utils import print_table


def print_student_menu():
    print('\n===== STUDENT MENU =====')
    print('1. Show all students')
    print('2. Add student')
    print('3. Back')


def show_all_students(cursor):

    try:

        cursor.execute('SELECT * FROM student_records')

        rows = cursor.fetchall()

        headers = [
            'Admno',
            'Student Name',
            'Class',
            'Section',
            'Roll No',
            'Book Issued',
            'Issue Date',
            'Return Status'
        ]

        print_table(rows, headers)

    except mysql.connector.Error as err:
        print(err)


def add_student(cursor, connection):

    try:

        name = input('Student Name: ').strip()
        class_name = input('Class: ').strip()
        section = input('Section: ').strip()

        roll_no = int(input('Roll Number: '))

    except ValueError:
        print('Invalid input.')
        return

    try:

        query = '''
        INSERT INTO student_records
        (Student_Name, Class, Section, Roll_No)
        VALUES (%s,%s,%s,%s)
        '''

        values = (
            name,
            class_name,
            section,
            roll_no
        )

        cursor.execute(query, values)

        connection.commit()

        print('Student added successfully.')

    except mysql.connector.Error as err:
        connection.rollback()
        print(err)


def student_menu(cursor, connection):

    while True:

        print_student_menu()

        choice = input('Enter choice: ').strip()

        if choice == '1':
            show_all_students(cursor)

        elif choice == '2':
            add_student(cursor, connection)

        elif choice == '3':
            break

        else:
            print('Invalid choice.')