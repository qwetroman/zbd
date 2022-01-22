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


def pobierz_druzyny():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT team_id, team_name,number_of_players, first_name, last_name FROM football_team inner join team_menager on team_menager.manager_id = football_team.manager_id")

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
        odlacz(cursor, connection)
    return teams


def pobierz_zawodnikow():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT first_name, last_name,phone_number, team_name, player_id from players left join football_team on players.team_id = football_team.team_id ORDER BY TEAM_NAME;")

    cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    for x in myresult:
        if x[3] == "NULL":
            x[3] = "Free agent"
        player = {'name': x[0],
                  'last_name': x[1],
                  'phone_number': x[2],
                  'team': x[3],
                  'id': x[4]}

        players.append(player)
    return players


def pobierz_druzyny_do_edycji(id):
    connection, cursor = polaczenie()
    komenda = (
        "SELECT team_id,team_name,number_of_players,first_name,last_name FROM football_team inner join team_menager on team_menager.manager_id=football_team.manager_id where team_id = %s;")

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
        odlacz(cursor, connection)
    return teams


def pobierz_sklad(id):
    connection, cursor = polaczenie()
    komenda = (
        "SELECT FIRST_NAME,LAST_NAME,PHONE_NUMBER,players.team_id,football_team.team_name FROM PLAYERS INNER JOIN FOOTBALL_TEAM ON FOOTBALL_TEAM.TEAM_ID = PLAYERS.TEAM_ID where players.team_id = %s;")

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
        odlacz(cursor, connection)
    return squads


def pobierz_sezony():
    connection, cursor = polaczenie()
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
        odlacz(cursor, connection)
    return seasons


def pobierz_stadiony():
    connection, cursor = polaczenie()
    komenda = ("SELECT * FROM STADION ORDER BY BEGGINING;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    stadiums = []
    for x in myresult:
        stadium = {'id': x[0],
                   'address': x[1],
                   'Capacity': x[2],
                   'Name': x[3]
                   }

        stadiums.append(stadium)
        odlacz(cursor, connection)
    return stadium


def delete_stadium(id):
    connection, cursor = polaczenie()
    komenda = "Delete from STADION where stadion_id=%s;"
    cursor.execute(komenda, (id,))
    odlacz(cursor, connection)
    return 0


def create_stadium(address, capacity, name):
    connection, cursor = polaczenie()
    komenda = "insert into stadion(address,number_of_seats,name) values (%s,%s,%s);"
    data=(address,capacity,name)
    cursor.execute(komenda, data);
    odlacz(cursor, connection)
    return 0


def update_stadium(id, address, capacity, name):
    connection, cursor = polaczenie()
    komenda = "update stadion SET address=%s,number_of_seats=%s,name=%s where stadion_id=%s;"
    data=(id, address, capacity, name)
    cursor.execute(komenda, data);
    odlacz(cursor, connection)
    return 0


def transfer_player(player_id, out_team, in_team, cost):
    connection, cursor = polaczenie()
    komenda = "call transfer_player(%s,%s,%s,%s);"
    komenda1 = "Select number_of_players from football_team where team_id = %s ;"
    komenda2 = "Select balance from budget inner join football_team on budget.budget_id=football_team.budget_id  " \
               "where football_team.team_id = %s ; "
    data = (int(out_team))
    cursor.execute(komenda1, data);
    connection.commit()
    myresult = cursor.fetchall()
    flaga = 0
    if int(myresult[0][0]) <= 23:
        flaga = 1
        odlacz(cursor, connection)
        return "Selling team do not have enough players!"
    cursor.execute(komenda2, int(in_team));
    myresult = cursor.fetchall()
    if int(myresult[0][0]) < int(cost):
        flaga = 1
        odlacz(cursor, connection)
        return "Buying team do not have enough money!"

    if flaga == 0:
        data = (int(player_id), int(out_team), int(in_team), int(cost))
        cursor.execute(komenda, data)
        connection.commit()
        odlacz(cursor, connection)
        return 0
    # cursor.execute(komenda)


def pobierz_gracza(id):
    connection, cursor = polaczenie()
    komenda = (
        "SELECT first_name,last_name,phone_number, player_id FROM PLAYERS where players.player_id = %s;")

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    for x in myresult:
        player = {'name': x[0],
                  'last_name': x[1],
                  'phone_number': x[2],
                  'id': x[3]
                  }

        players.append(player)
    return players


def add_team(name, season, adress, capacity, manager_name, manager_surname,
             manager_phone, balance, debt, profit, expenses):
    connection, cursor = polaczenie()
    komenda = "call create_team(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    komenda1 = "select season_id from season where season_name = %s"
    cursor.execute(komenda1, (season,))
    myresult = cursor.fetchall()
    season_id = myresult[0][0]
    data = (name, season_id, adress, capacity, manager_name, manager_surname,
            manager_phone, balance, debt, profit, expenses)
    cursor.execute(komenda, data);
    connection.commit()
    return 0


def add_player(name, surname, phone, team):
    connection, cursor = polaczenie()
    komenda = "call add_player(%s,%s,%s,%s);"
    komenda1 = "select team_id from football_team where team_name = %s"
    cursor.execute(komenda1, team)
    myresult = cursor.fetchall()
    team_id = myresult[0][0]
    data = (name, surname, phone, team_id)
    cursor.execute(komenda, data);
    connection.commit()
    odlacz(cursor, connection)
    return 0


def pobierz_coach():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT coach_id,first_name,last_name,phone_number,nationality,team_id,team_name FROM coach left join football_team on coach.team_id=football_team.team_id;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    coaches = []
    for x in myresult:
        coach = {'id': x[0],
                 'Name': x[1],
                 'Surname': x[2],
                 'Phone number': x[3],
                 'Nationality': x[4],
                 'Team': x[-1]
                 }

        coaches.append(coach)
        odlacz(cursor, connection)
    return coaches


def delete_coach(id):
    connection, cursor = polaczenie()
    komenda = "Delete from coach where coach_id=%s;"
    cursor.execute(komenda, (id,))
    odlacz(cursor, connection)
    return 0


def create_coach(first_name,last_name,phone_number,nationality):
    connection, cursor = polaczenie()
    komenda = "insert into coach(first_name,last_name,phone_number,nationality) values (%s,%s,%s,%s);"
    data=(first_name,last_name,phone_number,nationality)
    cursor.execute(komenda, data);
    odlacz(cursor, connection)
    return 0


def update_coach(first_name,last_name,phone_number,nationality):
    connection, cursor = polaczenie()
    komenda = "update stadion SET address=%s,number_of_seats=%s,name=%s where stadion_id=%s;"
    data=(first_name,last_name,phone_number,nationality)
    cursor.execute(komenda, first_name,last_name,phone_number,nationality);
    odlacz(cursor, connection)
    return 0
