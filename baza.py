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


def pobierz_druzyny(connection, cursor):
    komenda = ("SELECT team_id, team_name,number_of_players, first_name, last_name FROM football_team inner join team_menager on team_menager.manager_id = football_team.manager_id")

    cursor.execute(komenda)

    myresult = cursor.fetchall()
    teams = []
    for x in myresult:
        team = {'nazwa': x[1],
                'Number_of_players': x[2],
                'Manager_name': x[3],
                'Manager_lastname': x[4],
                'id': x[0],
                'Home_stadion': 'temp'}

        teams.append(team)
    return teams


def pobierz_zawodnikow(connection, cursor):
    komenda = ("SELECT first_name, last_name,phone_number, team_name from players inner join football_team on players.team_id = football_team.team_id ORDER BY TEAM_NAME;")

    cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    for x in myresult:
        player = {'name': x[0],
                  'last_name': x[1],
                  'phone_number': x[2],
                  'team': x[3]}

        players.append(player)
    return players


def pobierz_druzyny_do_edycji(connection, cursor, id):
    komenda = ("SELECT team_id,team_name,number_of_players,first_name,last_name FROM football_team inner join team_menager on team_menager.manager_id=football_team.manager_id where team_id = %s;")

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    teams = []
    for x in myresult:
        team = {'nazwa': x[1],
                'Number_of_players': x[2],
                'Manager_name': x[3],
                'Manager_lastname': x[4],
                'id': x[0],
                'Home_stadion': 'temp'}

        teams.append(team)
    return teams
