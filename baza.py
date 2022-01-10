import mysql.connector
from mysql.connector import Error


def polaczenie():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='PROJEKT',
                                             user='root',
                                             password='root1234',
                                             )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection, cursor
            cursor.execute("SELECT * FROM players")

            myresult = cursor.fetchall()

            for x in myresult:
                print(x)

    except Error as e:
        print("Error while connecting to MySQL", e)


def odlacz(cursor, connection):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")
