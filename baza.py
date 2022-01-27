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


def odlacz(connection, cursor):
    cursor.close()
    connection.close()
    print("MySQL connection is closed")


def pobierz_druzyny(connection, cursor):
    komenda = ("SELECT team_id, team_name,number_of_players, first_name, last_name,stadion_id,budget_id,season_id FROM football_team inner join team_menager on team_menager.manager_id = football_team.manager_id")

    cursor.execute(komenda)

    myresult = cursor.fetchall()
    teams = []
    for x in myresult:
        cursor.execute(
            "select name from stadion where stadion_id=%s", (int(x[5]),))
        stadion = cursor.fetchall()
        cursor.execute("select * from budget where budget_id=%s", (int(x[6]),))
        hajs = cursor.fetchall()
        if x[7] != None:
            cursor.execute(
                "select season_name from season where season_id=%s", (int(x[7]),))
            season = cursor.fetchall()
            season = season[0][0]
        else:
            season = None
        team = {'nazwa': x[1],
                'Number_of_players': x[2],
                'Manager_name': x[3],
                'Manager_lastname': x[4],
                'id': x[0],
                'Home_stadion': stadion[0][0],
                'balance': hajs[0][0],
                'debt': hajs[0][1],
                'profit': hajs[0][2],
                'expenses': hajs[0][3],
                'budget_id': hajs[0][4],
                'season_name': season
                }

        teams.append(team)
    return teams


def pobierz_zawodnikow(connection, cursor):
    komenda = ("SELECT first_name, last_name,phone_number, team_name, player_id from players left join football_team on players.team_id = football_team.team_id ORDER BY TEAM_NAME;")

    cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    print(myresult)
    for x in myresult:
        player = {'name': x[0],
                  'last_name': x[1],
                  'phone_number': x[2],
                  'team': x[3],
                  'id': x[4]}

        players.append(player)
    return players


def create_player(connection, cursor, name, last_name, phone):

    komenda = "insert into players(first_name, last_name, phone_number) values (%s, %s, %s)"
    dane = (name, last_name, phone)
    cursor.execute(komenda, dane)
    connection.commit()


def pobierz_wolne_stadiony(connection, cursor):
    komenda = ("select STADION.STADION_ID, STADION.NAME,FOOTBALL_TEAM.TEAM_NAME FROM STADION LEFT JOIN FOOTBALL_TEAM ON STADION.STADION_ID=FOOTBALL_TEAM.STADION_ID;")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    stadions = []
    for x in myresult:
        if x[2] == None:
            stadion = {'id': x[0],
                       'name': x[1],
                       }

            stadions.append(stadion)
    return stadions


def pobierz_wolnych_zawodnikow(connection, cursor):
    komenda = ("SELECT first_name, last_name,phone_number, team_name, player_id from players left join football_team on players.team_id = football_team.team_id ORDER BY TEAM_NAME;")
    cursor.execute(komenda)

    myresult = cursor.fetchall()
    players = []
    for x in myresult:
        if x[3] == None:
            player = {'name': x[0],
                      'last_name': x[1],
                      'phone_number': x[2],
                      'team': x[3],
                      'id': x[4]}

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
    komenda = ("SELECT FIRST_NAME,LAST_NAME,PHONE_NUMBER,players.team_id,football_team.team_name,players.player_id FROM PLAYERS left JOIN FOOTBALL_TEAM ON FOOTBALL_TEAM.TEAM_ID = PLAYERS.TEAM_ID where players.team_id = %s;")

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    squads = []
    for x in myresult:
        squad = {'name': x[0],
                 'last_name': x[1],
                 'phone_number': x[2],
                 'team_name': x[4],
                 'id': x[3],
                 'player_id': x[5]
                 }

        squads.append(squad)

    return squads


def pobierz_zawodnikow_i_numery():
    connection, cursor = polaczenie()
    komenda = ("SELECT FIRST_NAME,LAST_NAME,PHONE_NUMBER,team_id FROM PLAYERS;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    squads = []
    for x in myresult:
        squads.append(x[0] + " " + x[1] + " " + str(x[2]))

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


def pobierz_sezon(connection, cursor, id):
    komenda = ("SELECT * FROM SEASON where season_id = %s;")

    cursor.execute(komenda, (int(id),))
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


def transfer_player(connection, cursor, player_id, out_team, in_team, cost):
    komenda = "call transfer_player(%s,%s,%s,%s);"
    komenda1 = "Select number_of_players from football_team where team_id = %s;"
    komenda2 = "Select balance from budget inner join football_team on budget.budget_id=football_team.budget_id  " \
               "where football_team.team_id = %s; "
    data = (int(out_team),)
    print(data)
    cursor.execute(komenda1, data)
    myresult = cursor.fetchall()
    flaga = 0
    # if int(myresult[0][0]) <= 11:
    #     flaga = 1
    #     return "Selling team do not have enough players!"
    cursor.execute(komenda2, (int(in_team),))
    myresult = cursor.fetchall()
    # if int(myresult[0][0]) < int(cost):
    #     flaga = 1
    #     return "Buying team do not have enough money!"

    if flaga == 0:
        data = (int(player_id), int(out_team), int(in_team), int(cost))
        cursor.execute(komenda, data)
        connection.commit()
        return 0
    # cursor.execute(komenda)


def pobierz_gracza(connection, cursor, id):
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


def pobierz_gre(connection, cursor, id):
    komenda = ("select * from match_history where match_id = %s;")


def assign_player(connection, cursor, player_id, team_id):
    komenda = "update players set team_id=%s where player_id=%s"
    data = (team_id, player_id)
    cursor.execute(komenda, data)
    return 0


def add_team(connection, cursor, name, stadion_id, season_id, manager_id, balance, debt, profit, expenses, id1, id2, id3, id4, id5, id6, id7, id8, id9, id10, id11):
    komenda = "call create_team(%s,%s,%s,%s,%s,%s,%s,%s);"
    komenda2 = "select team_id from football_team where team_name = %s"
    data = (name, season_id, manager_id, stadion_id,
            balance, debt, profit, expenses)
    cursor.execute(komenda, data)
    cursor.execute(komenda2, (name,))
    idres = cursor.fetchall()
    assign_player(connection, cursor, id1, idres[0][0])
    assign_player(connection, cursor, id2, idres[0][0])
    assign_player(connection, cursor, id3, idres[0][0])
    assign_player(connection, cursor, id4, idres[0][0])
    assign_player(connection, cursor, id5, idres[0][0])
    assign_player(connection, cursor, id6, idres[0][0])
    assign_player(connection, cursor, id7, idres[0][0])
    assign_player(connection, cursor, id8, idres[0][0])
    assign_player(connection, cursor, id9, idres[0][0])
    assign_player(connection, cursor, id10, idres[0][0])
    assign_player(connection, cursor, id11, idres[0][0])

    connection.commit()

    return 0


def add_player(connection, cursor, name, surname, phone, team):
    komenda = "call add_player(%s,%s,%s,%s);"
    komenda1 = "select team_id from football_team where team_name = %s"
    cursor.execute(komenda1, team)
    myresult = cursor.fetchall()
    team_id = myresult[0][0]
    data = (name, surname, phone, team_id)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def pobierz_nazwy_druzyn(connection, cursor):

    komenda = "SELECT TEAM_NAME, team_id FROM FOOTBALL_TEAM"
    cursor.execute(komenda)
    result = cursor.fetchall()
    teams = []
    for x in result:
        teams.append(x[0] + " " + str(x[1]))

    return teams


def pobierz_stadiony(connection, cursor):
    komenda = ("SELECT * FROM STADION;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    stadiums = []
    for x in myresult:
        stadium = {'id': x[0],
                   'address': x[1],
                   'capacity': x[2],
                   'name': x[3]
                   }

        stadiums.append(stadium)

    return stadiums


def pobierz_stadion(connection, cursor, id):
    komenda = ("SELECT * FROM STADION where stadion_id = %s;")
    cursor.execute(komenda, (int(id),))
    myresult = cursor.fetchall()
    stadiums = []
    for x in myresult:
        stadium = {'id': x[0],
                   'address': x[1],
                   'capacity': x[2],
                   'name': x[3]
                   }

        stadiums.append(stadium)

    return stadiums


def pobierz_stadiony_team(connection, cursor):
    connection, cursor = polaczenie()
    komenda = ("SELECT * FROM STADION")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    stadiums = []
    for x in myresult:
        stadiums.append(x[3])

    return stadiums


def delete_stadium(id):
    connection, cursor = polaczenie()
    komenda = "Delete from STADION where stadion_id=%s;"
    cursor.execute(komenda, (int(id),))
    connection.commit()

    return 0


def create_stadium(address, capacity, name):
    connection, cursor = polaczenie()
    komenda = "insert into stadion(adress,number_of_sits,name) values (%s,%s,%s);"
    data = (address, capacity, name)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def update_stadium(connection, cursor, id, address, capacity, name):
    komenda = "update stadion SET adress=%s,number_of_sits=%s,name=%s where stadion_id=%s;"
    data = (address, capacity, name, id)
    cursor.execute(komenda, data)
    connection.commit()
    # cursor.execute(komenda, address, capacity, name, id)

    return 0


def pobierz_fizio():
    connection, cursor = polaczenie()

    komenda = (

        "SELECT physios_id,first_name,last_name,phone_number,physios_type,player_id,last_name FROM physios left join "
        "players on physios.player_id=players.player_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    physios = []

    for x in myresult:
        physio = {'id': x[0],

                  'Name': x[1],

                  'Surname': x[2],

                  'Phone number': x[3],

                  'Type': x[4],

                  'Employer': x[-1]

                  }

        physios.append(physio)

    return physios


def pobierz_coach():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT coach_id,first_name,last_name,phone_number,nationality,coach.team_id,team_name FROM coach left join football_team on coach.team_id=football_team.team_id;")

    cursor.execute(komenda)
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    coaches = []
    for x in myresult:
        coach = {'id': x[0],
                 'name': x[1],
                 'last_name': x[2],
                 'phone': x[3],
                 'nationality': x[4],
                 'team_name': x[-1]
                 }

        coaches.append(coach)

    return coaches


def get_coach_id(id):
    connection, cursor = polaczenie()
    komenda = "SELECT * FROM coach WHERE coach_id=%s"
    cursor.execute(komenda, (int(id),))
    myresult = cursor.fetchall()
    physios = []

    for x in myresult:
        physio = {'id': x[0],
                  'name': x[1],
                  'last_name': x[2],
                  'phone': x[3],
                  'nationality': x[4],
                  'team_name': x[-1]
                  }

        physios.append(physio)

    return physios


def delete_coach(id):
    connection, cursor = polaczenie()
    komenda = "Delete from coach where coach_id=%s;"
    cursor.execute(komenda, (id,))
    connection.commit()

    return 0


def create_coach(first_name, last_name, phone_number, nationality, id):
    connection, cursor = polaczenie()
    komenda = "insert into coach(first_name,last_name,phone_number,nationality, team_id) values (%s,%s,%s,%s,%s);"
    data = (first_name, last_name, phone_number, nationality, id)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def update_coach(first_name, last_name, phone_number, nationality):
    connection, cursor = polaczenie()
    komenda = "update stadion SET address=%s,number_of_seats=%s,name=%s where stadion_id=%s;"
    data = (first_name, last_name, phone_number, nationality)
    cursor.execute(komenda, first_name, last_name, phone_number, nationality)

    return 0


def pobierz_fizio():
    connection, cursor = polaczenie()

    komenda = (

        "SELECT physios_id,physios.first_name,physios.last_name,physios.phone_number,physios_type,players.first_name,players.last_name FROM physios left join players on physios.player_id=players.player_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    physios = []

    for x in myresult:
        physio = {'id': x[0],

                  'name': x[1],

                  'last_name': x[2],

                  'phone': x[3],

                  'type': x[4],

                  'player_last_name': x[-1],

                  'player_name': x[-2]

                  }

        physios.append(physio)

    return physios


def pobierz_physio_id(id):
    connection, cursor = polaczenie()
    komenda = "SELECT * FROM PHYSIOS WHERE PHYSIOS_ID=%s"
    cursor.execute(komenda, (int(id),))
    myresult = cursor.fetchall()
    physios = []

    for x in myresult:
        physio = {'id': x[0],

                  'name': x[1],

                  'last_name': x[2],

                  'phone': x[3],

                  'type': x[4],

                  'player_last_name': x[-1],

                  'player_name': x[-2]

                  }

        physios.append(physio)

    return physios


def delete_physio(id):
    connection, cursor = polaczenie()

    komenda = "Delete from physios where physios_id=%s;"

    cursor.execute(komenda, (id,))
    connection.commit()

    return 0


def create_physio(first_name, last_name, phone_number, physios_type, player):
    connection, cursor = polaczenie()
    name, surname, phone = player.split()
    id = get_player_id(name, surname, phone)
    komenda = "insert into physios(first_name,last_name,phone_number,physios_type,player_id) values (%s,%s,%s,%s,%s);"

    data = (first_name, last_name, phone_number, physios_type, id)

    cursor.execute(komenda, data)
    connection.commit()

    return 0


def get_player_id(name, surname, phone):
    connection, cursor = polaczenie()
    komenda = "select player_id from players where first_name =%s and last_name=%s and phone_number =%s"
    data = (name, surname, phone)
    cursor.execute(komenda, data)
    myresult = cursor.fetchall()
    return myresult[0][0]


def update_physios(physio_id, first_name, last_name, phone_number, physios_type, player_name, player_surname, player_phone):
    connection, cursor = polaczenie()
    player_id = get_player_id(player_name, player_surname, player_phone)

    komenda = "update physios SET first_name=%s,last_name=%s,phone_number=%s,physios_type=%s,player_id=%s where " \
              "physios_id=%s; "

    data = (first_name, last_name, phone_number,
            physios_type, player_id, physio_id)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def pobierz_managera():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT team_menager.manager_id,first_name,last_name,phone_number,team_name FROM team_menager left join football_team on team_menager.manager_id=football_team.manager_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    managers = []
    for x in myresult:
        if x[-1] == None:
            manager = {'id': x[0],
                       'Name': x[1],
                       'Surname': x[2],
                       'Phone_number': x[3],
                       'Employer': "Not employed"
                       }
        else:
            manager = {'id': x[0],
                       'Name': x[1],
                       'Surname': x[2],
                       'Phone_number': x[3],
                       'Employer': x[-1]
                       }
        managers.append(manager)

    return managers


def pobierz_wolnego_managera(connection, cursor):
    komenda = (
        "SELECT team_menager.manager_id,first_name,last_name,phone_number,team_name FROM team_menager left join football_team on team_menager.manager_id=football_team.manager_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    managers = []
    for x in myresult:
        if x[-1] == None:
            manager = {'id': x[0],
                       'Name': x[1],
                       'Surname': x[2],
                       'Phone_number': x[3],
                       'Employer': "Not employed"
                       }
            managers.append(manager)

    return managers


def delete_manager(id):
    connection, cursor = polaczenie()
    komenda = "Delete from team_menager where manager_id=%s;"
    cursor.execute(komenda, (id,))
    connection.commit()

    return 0


def update_manager(connection, cursor, id, name, last_name, phone):
    cursor.execute(
        "UPDATE TEAM_MENAGER SET FIRST_NAME=%s, last_name=%s,phone_number=%s where manager_id=%s", (name, last_name, phone, id))
    connection.commit()


def create_manager(first_name, last_name, phone_number):
    connection, cursor = polaczenie()
    komenda = "insert into team_menager(first_name,last_name,phone_number) values (%s,%s,%s);"
    data = (first_name, last_name, phone_number)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def get_manager_id(name, surname, phone):
    connection, cursor = polaczenie()
    komenda = "select manager_id from team_menager where first_name = %s and last_name = %s and phone_number = %s"
    cursor.execute(komenda, (name, surname, phone))
    myresult = cursor.fetchall()

    return myresult[0][0]


# def update_manager(first_name, last_name, phone_number, physios_type, player_id):
#    connection, cursor = polaczenie()
#    komenda = "update physios SET first_name=%s,last_name=%s,phone_number=%s,physios_type=%s,player_id=%s where " \
#
#              "physios_id=%s; "
#    data = (first_name, last_name, phone_number, physios_type, player_id,physio_id)
#    cursor.execute(komenda, data)
#    connection.commit()
#
#    return 0
def free_player(connection, cursor, id):
    komenda = "call free_player(%s)"
    cursor.execute(komenda, (id,))
    connection.commit()


def add_to_team(connection, cursor, player_id, team_id):
    komenda = "SELECT NUMBER_OF_PLAYERS FROM FOOTBALL_TEAM WHERE TEAM_ID=%s"
    dane = (int(team_id),)
    cursor.execute(komenda, dane)
    myresult = cursor.fetchall()
    if myresult[0][0] >= 23:
        return -1
    komenda = "update football_team set number_of_players=number_of_players+1 where team_id=%s"
    dane = (int(team_id),)
    cursor.execute(komenda, dane)
    komenda = "update players set team_id=%s where player_id = %s"
    dane = (int(team_id), int(player_id))
    cursor.execute(komenda, dane)
    connection.commit()


def delete_player(connection, cursor, id):
    komenda2 = "select team_id from players where player_id = %s; "
    komenda3 = "Select number_of_players from football_team where team_id=%s"
    komenda1 = "update football_team set number_of_players= number_of_players-1 where team_id=%s;"
    komenda = "Delete from players where player_id=%s;"
    cursor.execute(komenda2, (id,))
    myresult2 = cursor.fetchall()
    cursor.execute(komenda3, (myresult2[0][0],))
    myresult3 = cursor.fetchall()
    if len(myresult3) > 0:
        if int(myresult3[0][0]) <= 11:
            return "Team is too small"
    else:
        cursor.execute(komenda1, (myresult2[0][0],))
        cursor.execute(komenda, (id,))
        connection.commit()
        odlacz(cursor, connection)
        return 0


def delete_team(connection, cursor, id):

    # komenda2 = "select team_id from football_team where team_name = %s; "
    komenda1 = "update players set team_id= NULL where team_id=%s;"
    komenda = "Delete from football_team where team_id=%s;"
    komenda2 = "select budget_id from football_team where team_id=%s"
    komenda4 = "Delete from match_history where team1_id=%s or team2_id=%s"
    cursor.execute(komenda2, (int(id),))
    budżet = cursor.fetchall()
    komenda3 = "delete from budget where budget_id=%s"
    cursor.execute(komenda, (int(id),))
    cursor.execute(komenda4, (int(id), int(id)))

    cursor.execute(komenda3, (int(budżet[0][0]),))
    # cursor.execute(komenda2,(name,))
    # myresult2=cursor.fetchall()
    cursor.execute(komenda1, (int(id),))

    connection.commit()
    # odlacz(cursor, connection)
    return 0


def delete_season(connection, cursor, id):
    cursor.execute(
        "update football_team set season_id=Null where season_id=%s", (int(id),))
    cursor.execute("delete from season where season_id=%s", (int(id),))
    connection.commit()


def update_player(connection, cursor, id, name, last_name, phone):
    komenda = "update players set first_name=%s, last_name=%s, phone_number=%s where player_id=%s"
    dane = (name, last_name, phone, id)
    cursor.execute(komenda, dane)
    connection.commit()
    return 0


def create_history(connection, cursor, id_one, id_two, score_one, score_two, date, stadion_name):
    komenda = "select stadion_id from stadion where NAME =%s"
    dane = (stadion_name,)
    cursor.execute(komenda, dane)
    stadion_id = cursor.fetchall()[0][0]
    komenda2 = "INSERT INTO match_history(team1_id,team2_id,team1_score,team2_score,match_date,stadion_id) values(%s,%s,%s,%s,%s,%s)"
    dane = (id_one, id_two, score_one, score_two, date, stadion_id)
    cursor.execute(komenda2, dane)
    connection.commit()


def pobierz_historie(connection, cursor):
    komenda = 'select * from match_history'
    cursor.execute(komenda)
    wynik1 = cursor.fetchall()
    history = []
    for i in wynik1:
        cursor.execute(
            "select team_name from football_team where team_id=%s", (int(i[1]),))
        team1 = cursor.fetchall()

        cursor.execute(
            "select team_name from football_team where team_id=%s", (int(i[2]),))

        team2 = cursor.fetchall()
        cursor.execute(
            "select name from stadion where stadion_id=%s", (int(i[6]),))
        stadion = cursor.fetchall()
        gra = {
            'id': i[0],
            'team1': team1[0][0],
            'team2': team2[0][0],
            'team1_score': i[3],
            'team2_score': i[4],
            'data_gry': i[5],
            'stadion': stadion[0][0]
        }
        history.append(gra)
    return history


def delete_history(connection, cursor, id):
    komenda = "Delete from match_history where match_id=%s;"
    cursor.execute(komenda, (int(id),))
    connection.commit()
    return 0


def update_budget(connection, cursor, id, balance, debt, profit, expenses):
    komenda3 = "update budget SET balance=%s,dept=%s,profit=%s,expenses=%s where budget_id=%s;"
    data2 = (balance, debt, profit, expenses, id)
    cursor.execute(komenda3, data2)
    return 0


def update_team(connection, cursor, id, name, stadion_id, season_id, manager_id, balance, debt, profit, expenses):
    komenda = "update football_team set team_name=%s,stadion_id=%s,season_id=%s,manager_id=%s where team_id=%s"
    komenda2 = "select team_id,budget_id from football_team where team_id = %s"
    print(name)
    cursor.execute(komenda2, (int(id),))
    idres = cursor.fetchall()[0][1]
    data = (name, stadion_id, season_id, manager_id,
            id)
    komenda3 = "update budget SET balance=%s,dept=%s,profit=%s,expenses=%s where budget_id=%s;"
    data2 = (balance, debt, profit, expenses, idres)
    cursor.execute(komenda3, data2)
    cursor.execute(komenda, data)
    # update_budget(connection, cursor, idres, balance, debt, profit, expenses)
    # cursor.execute("select * from football_team")
    connection.commit()
    return 0


def pobierz_employee(connection, cursor):
    komenda = (

        "SELECT employee.employee_id,employee.first_name,employee.last_name,employee.phone_number,football_team.team_name FROM employee left join football_team on employee.team_id=football_team.team_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    employees = []
    for x in myresult:
        komenda1 = "SELECT * from receptionist where employee_id=%s"
        cursor.execute(komenda1, (x[0],))
        res = cursor.fetchall()
        if len(res) > 0:
            employee = {'id': x[0],

                        'name': x[1],

                        'last_name': x[2],

                        'phone': x[3],

                        'Employer': x[4],

                        'Recepcjonista': 'Tak'

                        }
            employees.append(employee)
        else:

            employee = {'id': x[0],

                        'name': x[1],

                        'last_name': x[2],

                        'phone': x[3],

                        'Employer': x[4],

                        'Recepcjonista': 'Nie'

                        }

            employees.append(employee)

    return employees


def update_employee(connection, cursor, first_name, last_name, phone_number, id):
    komenda = "update employee SET first_name=%s,last_name=%s,phone_number=%s where employee_id=%s;"
    data = (first_name, last_name, phone_number, id)
    cursor.execute(komenda, data)
    connection.commit()

    return 0


def create_employee(connection, cursor, first_name, last_name, phone_number, team_id, recepcjonista):
    komenda = "insert into employee(first_name,last_name,phone_number,team_id) values (%s,%s,%s,%s);"
    komenda1 = "insert into receptionist(employee_id,team_id) values(%s,%s);"
    data = (first_name, last_name, phone_number, team_id)
    cursor.execute(komenda, data)
    id = cursor.lastrowid
    data1 = (id, team_id)
    if recepcjonista == "Tak":
        cursor.execute(komenda1, data1)
    connection.commit()

    return 0


def delete_employee(connection, cursor, id):
    komenda0 = "select employee.first_name, receptionist.employee_id from employee left join receptionist on employee.employee_id = receptionist.employee_id where employee.employee_id=%s"
    cursor.execute(komenda0, (int(id),))
    res = cursor.fetchall()
    if res[0][1] == None:
        komenda = "Delete from employee where employee_id=%s;"
        cursor.execute(komenda, (int(id),))
    else:
        cursor.execute(
            "Delete from receptionist where employee_id=%s", (int(id),))
        komenda = "Delete from employee where employee_id=%s;"
        cursor.execute(komenda, (int(id),))
    connection.commit()

    return 0
