import mysql.connector
from datetime import datetime
from utils import print_table


def print_book_menu():
    print('\n===== BOOK MENU =====')
    print('1. Show all books')
    print('2. Search book')
    print('3. Add book')
    print('4. Update book')
    print('5. Delete book')
    print('6. Back')


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

        print_table(rows, headers)

    except mysql.connector.Error as err:
        print(err)


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

            print_table(rows, headers)

        else:
            print('No books found.')

    except mysql.connector.Error as err:
        print(err)


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
        print(err)


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

        print('Book updated.')

    except mysql.connector.Error as err:
        connection.rollback()
        print(err)


def delete_book(cursor, connection):

    isbn = input('Enter ISBN: ').strip()

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
        print(err)


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