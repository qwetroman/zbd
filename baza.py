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
        "SELECT team_id, team_name,number_of_players, first_name, last_name FROM football_team inner join "
        "team_menager on team_menager.manager_id = football_team.manager_id")

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
        "SELECT first_name, last_name,phone_number, team_name, player_id from players left join football_team on "
        "players.team_id = football_team.team_id ORDER BY TEAM_NAME;")

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

def get_budget_id(id):
    connection,cursor = polaczenie()
    komenda = "select balance, debt, profit, expenses from budget left join football_club on budget.budget_id= football_team.budget_id"
    cursor.execute(komenda,(id,))
    myresult=cursor.fetchall()
    return myresult[0][0],myresult[0][1],myresult[0][2],myresult[0][3]


def pobierz_druzyny_do_edycji(id):
    connection, cursor = polaczenie()
    komenda = (
        "SELECT team_id,team_name,number_of_players,first_name,last_name FROM football_team inner join team_menager "
        "on team_menager.manager_id=football_team.manager_id where team_id = %s;")

    cursor.execute(komenda, (int(id),))
    # cursor.execute(komenda)

    myresult = cursor.fetchall()
    teams = []
    for x in myresult:
        balance,debt,profit,expenses=get_budget_id(id)
        team = {'nazwa': x[1],
                'Number_of_players': x[2],
                'Manager_name': x[3],
                'Manager_lastname': x[4],
                'id': x[0],
                'Home_stadion': 'temp',
                'Balance': balance,
                'Debt':debt,
                'Profit':profit,
                'Expenses':expenses}

        teams.append(team)
        odlacz(cursor, connection)
    return teams


def pobierz_sklad(id):
    connection, cursor = polaczenie()
    komenda = (
        "SELECT FIRST_NAME,LAST_NAME,PHONE_NUMBER,players.team_id,football_team.team_name FROM PLAYERS INNER JOIN "
        "FOOTBALL_TEAM ON FOOTBALL_TEAM.TEAM_ID = PLAYERS.TEAM_ID where players.team_id = %s;")

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
    komenda = "SELECT * FROM SEASON ORDER BY BEGGINING;"

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
    komenda = "SELECT * FROM STADION ORDER BY BEGGINING;"

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
    komenda1 = "select * from football_team where stadion_id=%s;"
    cursor.execute(komenda1, id)
    myresult = cursor.fetchall()
    if myresult[0][0] != 'NULL':
        return "This stadium is occupied by team"
    else:
        komenda = "Delete from STADION where stadion_id=%s;"
        cursor.execute(komenda, (id,))
        odlacz(cursor, connection)
        return 0


def create_stadium(address, capacity, name):
    connection, cursor = polaczenie()
    komenda = "insert into stadion(address,number_of_seats,name) values (%s,%s,%s);"
    data = (address, capacity, name)
    cursor.execute(komenda, data)
    odlacz(cursor, connection)
    return 0


def update_stadium(id, address, capacity, name):
    connection, cursor = polaczenie()
    komenda = "update stadion SET address=%s,number_of_seats=%s,name=%s where stadion_id=%s;"
    data = (id, address, capacity, name)
    cursor.execute(komenda, data)
    odlacz(cursor, connection)
    return 0


def transfer_player(player_id, out_team, in_team, cost):
    connection, cursor = polaczenie()
    komenda = "call transfer_player(%s,%s,%s,%s);"
    komenda1 = "Select number_of_players from football_team where team_id = %s ;"
    komenda2 = "Select balance from budget inner join football_team on budget.budget_id=football_team.budget_id  " \
               "where football_team.team_id = %s ; "
    data = (int(out_team))
    cursor.execute(komenda1, data)
    connection.commit()
    myresult = cursor.fetchall()
    flaga = 0
    if int(myresult[0][0]) <= 23:
        flaga = 1
        odlacz(cursor, connection)
        return "Selling team do not have enough players!"
    cursor.execute(komenda2, int(in_team))
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
    cursor.execute(komenda, data)
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
    cursor.execute(komenda, data)
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


def create_coach(first_name, last_name, phone_number, nationality):
    connection, cursor = polaczenie()
    komenda = "insert into coach(first_name,last_name,phone_number,nationality) values (%s,%s,%s,%s);"
    data = (first_name, last_name, phone_number, nationality)
    cursor.execute(komenda, data)
    odlacz(cursor, connection)
    return 0


def update_coach(first_name, last_name, phone_number, nationality):
    connection, cursor = polaczenie()
    komenda = "update stadion SET address=%s,number_of_seats=%s,name=%s where stadion_id=%s;"
    data = (first_name, last_name, phone_number, nationality)
    cursor.execute(komenda, first_name, last_name, phone_number, nationality)
    odlacz(cursor, connection)
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

        odlacz(cursor, connection)

    return physios


def delete_physio(id):
    connection, cursor = polaczenie()

    komenda = "Delete from physios where physios_id=%s;"

    cursor.execute(komenda, (id,))
    connection.commit()
    odlacz(cursor, connection)

    return 0


def create_physio(first_name, last_name, phone_number, physios_type):
    connection, cursor = polaczenie()

    komenda = "insert into physios(first_name,last_name,phone_number,physios_type) values (%s,%s,%s,%s);"

    data = (first_name, last_name, phone_number, physios_type)

    cursor.execute(komenda, data)
    connection.commit()
    odlacz(cursor, connection)

    return 0

def get_player_id(name,surname,phone):
    connection,cursor =polaczenie()
    komenda = "select player_id form players where first_name =%s and last_name=% and phone_number =%s"
    data=(name,surname,phone)
    cursor.execute(komenda,data)
    myresult=cursor.fetchall()
    return myresult[0][0]


def update_physios(physio_id, first_name, last_name, phone_number, physios_type, player_name,player_surname,player_phone):
    connection, cursor = polaczenie()
    player_id=get_player_id(player_name,player_surname,player_phone)

    komenda = "update physios SET first_name=%s,last_name=%s,phone_number=%s,physios_type=%s,player_id=%s where " \
              "physios_id=%s; "

    data = (first_name, last_name, phone_number, physios_type, player_id, physio_id)
    cursor.execute(komenda, data)
    connection.commit()
    odlacz(cursor, connection)

    return 0


def pobierz_managera():
    connection, cursor = polaczenie()
    komenda = (
        "SELECT team_menager.manager_id,first_name,last_name,phone_number,team_name FROM team_menager left join "

        "football_team on team_menager.manager_id=football_team.manager_id")
    cursor.execute(komenda)
    myresult = cursor.fetchall()
    managers = []
    for x in myresult:
        if x[-1] == 'NULL':
            x[-1] = 'Not employed'
        manager = {'id': x[0],
                   'Name': x[1],
                   'Surname': x[2],
                   'Phone number': x[3],
                   'Employer': x[-1]
                   }
        managers.append(manager)
        odlacz(cursor, connection)
    return managers


def delete_manager(id):
  connection, cursor = polaczenie()
  komenda = "Delete from team_menager where manager_id=%s;"
  cursor.execute(komenda, (id,))
  connection.commit()
  odlacz(cursor, connection)
  return 0


def create_manager(first_name, last_name, phone_number):
  connection, cursor = polaczenie()
  komenda = "insert into team_menager(first_name,last_name,phone_number) values (%s,%s,%s);"
  data = (first_name, last_name, phone_number)
  cursor.execute(komenda, data)
  connection.commit()
  odlacz(cursor, connection)
  return 0

def get_team_id(name):
    connection, cursor = polaczenie()
    komenda = "select team_id from football_team where team_name = %s"
    cursor.execute(komenda,(name,))
    myresult=cursor.fetchall()
    odlacz(cursor,connection)
    return myresult[0][0]

def get_manager_id(name,surname,phone):
    connection, cursor = polaczenie()
    komenda = "select manager_id from team_menager where first_name = %s and last_name = %s and phone_number = %s"
    cursor.execute(komenda,(name,surname,phone))
    myresult=cursor.fetchall()
    odlacz(cursor,connection)
    return myresult[0][0]


 def update_manager(first_name, last_name, phone_number,team):
    connection, cursor = polaczenie()
    team_id=get_team_id(team)
    manager_id=get_manager_id(first_name,last_name,phone_number)
    komenda = "update team_menager SET first_name=%s,last_name=%s,phone_number=%s,team_id=%s where " \
              "manager_id=%s; "
    data = (first_name, last_name, phone_number, team_id, manager_id)
    cursor.execute(komenda, data)
    connection.commit()
    odlacz(cursor, connection)
    return 0
def free_player(id):
    connection, cursor = polaczenie()
    komenda = "call free_player(%s)"
    cursor.execute(komenda, (id,))
    connection.commit()
    odlacz(cursor, connection)
    return 0
def get_all_manager():
    connection,cursor = polaczenie()
    komenda ="select first_name,last_name,phone_number from team_menager "
    cursor.execute(komenda)
    myresult=cursor.fetchall()
    managers=[]
    for x in myresult:
        manager=x[0]+x[1]+x[2]
        managers.append(manager)
    return managers
