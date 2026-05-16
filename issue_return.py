import mysql.connector
from datetime import datetime, timedelta


def issue_book(cursor, connection):

    student_id = input('Enter Student Admno: ').strip()
    isbn = input('Enter Book ISBN: ').strip()

    try:

        cursor.execute(
            'SELECT * FROM student_records WHERE Admno = %s',
            (student_id,)
        )

        student = cursor.fetchone()

        if not student:
            print('Student not found.')
            return

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

        cursor.execute(
            '''
            UPDATE books_records
            SET Quantity = Quantity - 1
            WHERE ISBN = %s
            ''',
            (isbn,)
        )

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

        due_date = issue_date + timedelta(days=7)

        print('Book issued successfully.')
        print('Due Date:', due_date)

    except mysql.connector.Error as err:
        connection.rollback()
        print(err)


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

        cursor.execute(
            '''
            UPDATE books_records
            SET Quantity = Quantity + 1
            WHERE Name = %s
            ''',
            (book_name,)
        )

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
        print(err)