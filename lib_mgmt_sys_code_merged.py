# =========================
# LIBRARY MANAGEMENT SYSTEM
# =========================

import mysql.connector
from datetime import datetime, timedelta
from tabulate import tabulate


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'B1P2D3R4',
    'database': 'library_management_system',
    'charset': 'utf8mb4',
    'auth_plugin': 'mysql_native_password'
}


# =========================
# DATABASE CONNECTION
# =========================

def connect_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection

    except mysql.connector.Error as err:
        print('Database connection failed.')
        print(err)
        return None


# =========================
# MAIN MENU
# =========================

def print_main_menu():
    print('\n===== MAIN MENU =====')
    print('1. Book Records')
    print('2. Student Records')
    print('3. Teacher Records')
    print('4. Issue Book')
    print('5. Return Book')
    print('6. Exit')


# =========================
# BOOK MENU
# =========================

def print_book_menu():
    print('\n===== BOOK MENU =====')
    print('1. Show all books')
    print('2. Search book')
    print('3. Add book')
    print('4. Update book')
    print('5. Delete book')
    print('6. Back')


# =========================
# STUDENT MENU
# =========================

def print_student_menu():
    print('\n===== STUDENT MENU =====')
    print('1. Show all students')
    print('2. Add student')
    print('3. Back')


# =========================
# TEACHER MENU
# =========================

def print_teacher_menu():
    print('\n===== TEACHER MENU =====')
    print('1. Show all teachers')
    print('2. Add teacher')
    print('3. Back')


# =========================
# SHOW BOOKS
# =========================

def show_all_books(cursor):
    try:
        cursor.execute('SELECT * FROM books_records')
        rows = cursor.fetchall()

        headers = [
            'ISBN',
            'Name',
            'Publication',
            'Author',
            'Genre',
            'Quantity',
            'Purchase Date',
            'Price'
        ]

        print('\nALL BOOK RECORDS\n')
        print(tabulate(rows, headers=headers, tablefmt='grid'))

    except mysql.connector.Error as err:
        print('Error:', err)


# =========================
# SEARCH BOOK
# =========================

def search_book(cursor):
    keyword = input('Enter book name/author/genre: ').strip()

    try:
        query = '''
        SELECT * FROM books_records
        WHERE Name LIKE %s
        OR Author LIKE %s
        OR Genre LIKE %s
        '''

        value = f'%{keyword}%'

        cursor.execute(query, (value, value, value))

        rows = cursor.fetchall()

        if rows:
            headers = [
                'ISBN',
                'Name',
                'Publication',
                'Author',
                'Genre',
                'Quantity',
                'Purchase Date',
                'Price'
            ]

            print(tabulate(rows, headers=headers, tablefmt='grid'))

        else:
            print('No matching books found.')

    except mysql.connector.Error as err:
        print('Search Error:', err)


# =========================
# ADD BOOK
# =========================

def add_book(cursor, connection):

    try:
        name = input('Book Name: ').strip()
        publication = input('Publication: ').strip()
        author = input('Author: ').strip()
        genre = input('Genre: ').strip()

        quantity = int(input('Quantity: '))
        price = float(input('Price: '))

        purchase_date = input('Purchase Date (YYYY-MM-DD): ')
        datetime.strptime(purchase_date, '%Y-%m-%d')

    except ValueError:
        print('Invalid input.')
        return

    try:

        # duplicate check
        cursor.execute(
            'SELECT * FROM books_records WHERE Name = %s AND Author = %s',
            (name, author)
        )

        existing = cursor.fetchone()

        if existing:
            print('Book already exists.')
            return

        query = '''
        INSERT INTO books_records
        (Name, Publication, Author, Genre, Quantity, Date_of_purchase, Price)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        '''

        values = (
            name,
            publication,
            author,
            genre,
            quantity,
            purchase_date,
            price
        )

        cursor.execute(query, values)

        connection.commit()

        print('Book added successfully.')

    except mysql.connector.Error as err:
        connection.rollback()
        print('Database Error:', err)


# =========================
# UPDATE BOOK
# =========================

def update_book(cursor, connection):

    isbn = input('Enter ISBN: ').strip()

    cursor.execute(
        'SELECT * FROM books_records WHERE ISBN = %s',
        (isbn,)
    )

    record = cursor.fetchone()

    if not record:
        print('Book not found.')
        return

    fields = [
        'Name',
        'Publication',
        'Author',
        'Genre',
        'Quantity',
        'Price'
    ]

    print('\nChoose field:')
    for index, field in enumerate(fields, start=1):
        print(f'{index}. {field}')

    choice = input('Enter choice: ').strip()

    if not choice.isdigit():
        print('Invalid choice.')
        return

    choice = int(choice)

    if choice < 1 or choice > len(fields):
        print('Invalid choice.')
        return

    field = fields[choice - 1]

    new_value = input(f'Enter new {field}: ').strip()

    try:

        query = f'''
        UPDATE books_records
        SET {field} = %s
        WHERE ISBN = %s
        '''

        cursor.execute(query, (new_value, isbn))

        connection.commit()

        print('Book updated successfully.')

    except mysql.connector.Error as err:
        connection.rollback()
        print('Update Error:', err)


# =========================
# DELETE BOOK
# =========================

def delete_book(cursor, connection):

    isbn = input('Enter ISBN to delete: ').strip()

    try:

        cursor.execute(
            'DELETE FROM books_records WHERE ISBN = %s',
            (isbn,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            print('Book deleted.')

        else:
            print('Book not found.')

    except mysql.connector.Error as err:
        connection.rollback()
        print('Delete Error:', err)


# =========================
# ISSUE BOOK
# =========================

def issue_book(cursor, connection):

    student_id = input('Enter Student Admno: ').strip()
    isbn = input('Enter Book ISBN: ').strip()

    try:

        # student check
        cursor.execute(
            'SELECT * FROM student_records WHERE Admno = %s',
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print('Student not found.')
            return

        # book check
        cursor.execute(
            'SELECT Name, Quantity FROM books_records WHERE ISBN = %s',
            (isbn,)
        )

        book = cursor.fetchone()

        if not book:
            print('Book not found.')
            return

        book_name = book[0]
        quantity = book[1]

        if quantity <= 0:
            print('Book not available.')
            return

        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=7)

        # reduce quantity
        cursor.execute(
            '''
            UPDATE books_records
            SET Quantity = Quantity - 1
            WHERE ISBN = %s
            ''',
            (isbn,)
        )

        # assign book
        cursor.execute(
            '''
            UPDATE student_records
            SET Book_Issued = %s,
                Issue_Date = %s,
                Return_Status = %s
            WHERE Admno = %s
            ''',
            (
                book_name,
                issue_date,
                'Not Returned',
                student_id
            )
        )

        connection.commit()

        print('Book issued successfully.')
        print('Due Date:', due_date)

    except mysql.connector.Error as err:
        connection.rollback()
        print('Issue Error:', err)


# =========================
# RETURN BOOK
# =========================

def return_book(cursor, connection):

    student_id = input('Enter Student Admno: ').strip()

    try:

        cursor.execute(
            '''
            SELECT Book_Issued, Issue_Date
            FROM student_records
            WHERE Admno = %s
            ''',
            (student_id,)
        )

        record = cursor.fetchone()

        if not record:
            print('Student not found.')
            return

        book_name = record[0]
        issue_date = record[1]

        if not book_name:
            print('No book issued.')
            return

        today = datetime.now().date()

        fine = 0

        if issue_date:
            days = (today - issue_date).days

            if days > 7:
                fine = (days - 7) * 5

        # increase quantity
        cursor.execute(
            '''
            UPDATE books_records
            SET Quantity = Quantity + 1
            WHERE Name = %s
            ''',
            (book_name,)
        )

        # clear student issue
        cursor.execute(
            '''
            UPDATE student_records
            SET Book_Issued = NULL,
                Issue_Date = NULL,
                Return_Status = 'Returned'
            WHERE Admno = %s
            ''',
            (student_id,)
        )

        connection.commit()

        print('Book returned successfully.')

        if fine > 0:
            print(f'Fine: ₹{fine}')

        else:
            print('No fine.')

    except mysql.connector.Error as err:
        connection.rollback()
        print('Return Error:', err)


# =========================
# SHOW STUDENTS
# =========================

def show_all_students(cursor):

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

    print(tabulate(rows, headers=headers, tablefmt='grid'))


# =========================
# ADD STUDENT
# =========================

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
        print('Database Error:', err)


# =========================
# SHOW TEACHERS
# =========================

def show_all_teachers(cursor):

    cursor.execute('SELECT * FROM teacher_records')

    rows = cursor.fetchall()

    headers = [
        'Id_No',
        'Teacher Name',
        'Book Issued',
        'Issue Date',
        'Return Status'
    ]

    print(tabulate(rows, headers=headers, tablefmt='grid'))


# =========================
# ADD TEACHER
# =========================

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
        print('Database Error:', err)


# =========================
# BOOK MENU LOGIC
# =========================

def book_menu(cursor, connection):

    while True:

        print_book_menu()

        choice = input('Enter choice: ').strip()

        if choice == '1':
            show_all_books(cursor)

        elif choice == '2':
            search_book(cursor)

        elif choice == '3':
            add_book(cursor, connection)

        elif choice == '4':
            update_book(cursor, connection)

        elif choice == '5':
            delete_book(cursor, connection)

        elif choice == '6':
            break

        else:
            print('Invalid choice.')


# =========================
# STUDENT MENU LOGIC
# =========================

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


# =========================
# TEACHER MENU LOGIC
# =========================

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


# =========================
# MAIN FUNCTION
# =========================

def main():

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

    print('\n===== LIBRARY MANAGEMENT SYSTEM =====')

    try:

        while True:

            print_main_menu()

            choice = input('Enter choice: ').strip()

            if choice == '1':
                book_menu(cursor, connection)

            elif choice == '2':
                student_menu(cursor, connection)

            elif choice == '3':
                teacher_menu(cursor, connection)

            elif choice == '4':
                issue_book(cursor, connection)

            elif choice == '5':
                return_book(cursor, connection)

            elif choice == '6':
                print('Exiting program...')
                break

            else:
                print('Invalid choice.')

    except KeyboardInterrupt:
        print('\nProgram interrupted.')

    finally:
        cursor.close()
        connection.close()


# =========================
# START PROGRAM
# =========================

if __name__ == '__main__':
    main()