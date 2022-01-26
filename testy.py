from baza import polaczenie, odlacz


def get_manager_id(name, surname, phone):
    connection, cursor = polaczenie()
    komenda = "select manager_id from team_menager where first_name = %s and last_name = %s and phone_number = %s"
    cursor.execute(komenda, (name, surname, phone))
    myresult = cursor.fetchall()
    odlacz(cursor, connection)
    return myresult[0][0]


print(get_manager_id("Mircea", "Lucesku", "953892130"))
