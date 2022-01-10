from flask import Flask, render_template, flash, redirect, url_for
from forms import AddTeamForm, AddGameForm, AddStadionForm
from baza import polaczenie, odlacz
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e185681a407ace961e0bf2fdcdced1c7'

connection, cursor = polaczenie()


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
                'Home_stadion': 'temp'}

        teams.append(team)
    return teams


# Druzyny = [
#
#     {
#         'nazwa': 'temp',
#         'Id': 10000,
#         'Number_of_players': 12,
#         'Coach_id': 10001,
#         'Manager_id': 10002,
#         'Home_stadion': 'temp'
#
#
#     },
#
#     {
#         'nazwa': 'temp2',
#         'Id': 10001,
#         'Number_of_players': 17,
#         'Coach_id': 10001,
#         'Manager_id': 10002,
#         'Home_stadion': 'Zlocieniec'
#
#     }
# ]

History = [
    {
        'team1': 'temp',
        'team2': 'temp',
        'data_gry': 'temp2',
        'stadion': 'nasd'
    }
]
Stadiony = [
    {
        'adres': 'temp',
        'seats': 'temp2'
    }


]


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    connection, cursor = polaczenie()
    Druzyny = pobierz_druzyny(connection, cursor)
    odlacz(cursor, connection)
    return render_template('about.html', title='Druzyny', posts=Druzyny)


@app.route('/match_history')
def match_history():
    return render_template('match_history.html', title='Historia gier',
                           posts=History)


@app.route('/stadions')
def stadions():
    return render_template('stadions.html', title='Stadiony',
                           posts=Stadiony)


@app.route('/AddTeam', methods=['GET', 'POST'])
def AddTeam():
    form = AddTeamForm()
    if form.validate_on_submit():
        flash(
            f'Druzyna {form.TeamName.data} zostala pomyslnie dodana',
            'success')

        return redirect(url_for('home'))

    return render_template('addteam.html',
                           form=form, title='Dodawanie druzyny')


@app.route('/add_game', methods=['GET', 'POST'])
def AddGame():
    form = AddGameForm()
    if form.validate_on_submit():
        flash(
            'Gra zostala pomyslnie dodana',
            'success')

        return redirect(url_for('home'))

    return render_template('add_game.html',
                           form=form, title='Dodawanie gry')


@app.route('/add_stadion', methods=['GET', 'POST'])
def AddStadion():
    form = AddStadionForm()
    if form.validate_on_submit():
        flash(
            'Stadion został pomyślnie dodany',
            'success')

        return redirect(url_for('home'))

    return render_template('add_stadion.html',
                           form=form, title='Dodawanie stadionu')


if __name__ == '__main__':
    app.run(debug=True)
