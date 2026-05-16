import mysql.connector
from utils import print_table


def print_teacher_menu():
    print('\n===== TEACHER MENU =====')
    print('1. Show all teachers')
    print('2. Add teacher')
    print('3. Back')


def show_all_teachers(cursor):

    try:

        cursor.execute('SELECT * FROM teacher_records')

        rows = cursor.fetchall()

        headers = [
            'Id_No',
            'Teacher Name',
            'Book Issued',
            'Issue Date',
            'Return Status'
        ]

        print_table(rows, headers)

    except mysql.connector.Error as err:
        print(err)


def add_teacher(cursor, connection):

    name = input('Teacher Name: ').strip()

    try:

        query = '''
        INSERT INTO teacher_records
        (Teacher_Name)
        VALUES (%s)
        '''

        cursor.execute(query, (name,))

        connection.commit()

        print('Teacher added successfully.')

    except mysql.connector.Error as err:
        connection.rollback()
        print(err)


def teacher_menu(cursor, connection):

    while True:

        print_teacher_menu()

        choice = input('Enter choice: ').strip()

        if choice == '1':
            show_all_teachers(cursor)

        elif choice == '2':
            add_teacher(cursor, connection)

        elif choice == '3':
            break

        else:
            print('Invalid choice.')