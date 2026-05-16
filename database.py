import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YourPasswordHere',
    'database': 'library_management_system',
    'charset': 'utf8mb4',
    'auth_plugin': 'mysql_native_password'
}


def connect_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection

    except mysql.connector.Error as err:
        print('Database connection failed.')
        print(err)
        return None