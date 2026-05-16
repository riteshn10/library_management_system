from database import connect_database

from books import book_menu
from students import student_menu
from teachers import teacher_menu

from issue_return import issue_book
from issue_return import return_book


def print_main_menu():

    print('\n===== LIBRARY MANAGEMENT SYSTEM =====')

    print('1. Book Records')
    print('2. Student Records')
    print('3. Teacher Records')
    print('4. Issue Book')
    print('5. Return Book')
    print('6. Exit')


def main():

    connection = connect_database()

    if connection is None:
        return

    cursor = connection.cursor()

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


if __name__ == '__main__':
    main()