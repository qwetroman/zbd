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


def pobierz_sklad(connection, cursor, id):
    komenda = ("SELECT FIRST_NAME,LAST_NAME,PHONE_NUMBER,players.team_id,football_team.team_name FROM PLAYERS INNER JOIN FOOTBALL_TEAM ON FOOTBALL_TEAM.TEAM_ID = PLAYERS.TEAM_ID where players.team_id = %s;")

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    squads = []
    for x in myresult:
        squad = {'name': x[0],
                 'last_name': x[1],
                 'phone_number': x[2],
                 'team_name': x[4],
                 'id': x[3]
                 }

        squads.append(squad)
    return squads


def pobierz_sezony(connection, cursor):
    komenda = ("SELECT * FROM SEASON ORDER BY BEGGINING;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    seasons = []
    for x in myresult:
        season = {'name': x[2],
                  'country': x[1],
                  'beggining': x[3],
                  'end': x[4],
                  'id': x[0]
                  }

        seasons.append(season)
    return seasons
def transfer_player(connection, cursor, player_id,out_team,in_team,cost):
    komenda = "call transfer_player(%s,%s,%s,%s);"
    komenda1 = "Select number_of_players from football_team where team_id = %s ;"
    komenda2 = "Select balance from budget inner join football_team on budget.budget_id=football_team.budget_id  " \
               "where football_team.team_id = %s ; "
    cursor.execute(komenda1,int(out_team));
    myresult = cursor.fetchall()
    flaga=0
    if int(myresult[0][0])<=23:
        flaga=1
        return "Selling team do not have enough players!"
    cursor.execute(komenda2, int(in_team));
    myresult = cursor.fetchall()
    if int(myresult[0][0]) < int(cost):
        flaga=1
        return "Buying team do not have enough money!"

    if flaga==0:
        cursor.execute(komenda,int(player_id),int(out_team),int(in_team),int(cost))
        return 0
    # cursor.execute(komenda)

def pobierz_gracza(connection, cursor, id):
    komenda = "SELECT first_name,last_name,phone_number FROM PLAYERS where players.player_id = %s;"

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    for x in myresult:
        player = {'name': x[0],
                 'last_name': x[1],
                 'phone_number': x[2],
                 }

        players.append(player)
    return players
