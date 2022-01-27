from baza import polaczenie, odlacz


def get_manager_id(name, surname, phone):
    connection, cursor = polaczenie()
    komenda = "select manager_id from team_menager where first_name = %s and last_name = %s and phone_number = %s"
    cursor.execute(komenda, (name, surname, phone))
    myresult = cursor.fetchall()
    odlacz(cursor, connection)
    return myresult[0][0]


def pobierz_historie(connection, cursor):
    komenda = 'select * from match_history'
    cursor.execute(komenda)
    wynik1 = cursor.fetchall()
    history = []
    for i in wynik1:
        cursor.execute(
            "select team_name from football_team where team_id=%s", (int(i[1]),))
        team1 = cursor.fetchall()
        print(team1)

        cursor.execute(
            "select team_name from football_team where team_id=%s", (int(i[2]),))

        team2 = cursor.fetchall()
        print(team2)
        cursor.execute(
            "select name from stadion where stadion_id=%s", (int(i[6]),))
        stadion = cursor.fetchall()
        gra = {
            'team1': team1[0][0],
            'team2': team2[0][0],
            'team1_score': i[3],
            'team2_score': i[4],
            'data_gry': i[5],
            'stadion': stadion
        }
        history.append(gra)
    return history


print("mama tata".split()[-1])
