from flask import Flask, render_template, flash, redirect, url_for, request
from forms import AddTeamForm, AddGameForm, AddStadionForm, AddPlayerForm, EditTeamForm
from baza import polaczenie, odlacz, pobierz_druzyny, pobierz_zawodnikow, pobierz_druzyny_do_edycji
# import mysql.connector
# from mysql.connector import Error

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e185681a407ace961e0bf2fdcdced1c7'


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


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/teams', methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        flash(
            'Drużyna została pomyślnie edytowana',
            'success')
        print(request.form.get('TeamName'))
        return redirect(url_for('about'))
    connection, cursor = polaczenie()
    Druzyny = pobierz_druzyny(connection, cursor)
    odlacz(cursor, connection)
    return render_template('teams.html', title='Druzyny', posts=Druzyny)


@app.route('/match_history')
def match_history():
    return render_template('match_history.html', title='Historia gier',
                           posts=History)


@app.route('/stadions')
def stadions():
    return render_template('stadions.html', title='Stadiony',
                           posts=Stadiony)


@app.route('/players')
def players():
    connection, cursor = polaczenie()
    Gracze = pobierz_zawodnikow(connection, cursor)
    odlacz(cursor, connection)
    return render_template('players.html', title="Gracze", posts=Gracze)


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


@app.route('/add_player', methods=['GET', 'POST'])
def AddPlayer():
    form = AddPlayerForm()
    if form.validate_on_submit():
        flash(
            'Zawodnik został pomyślnie dodany',
            'success')

        return redirect(url_for('home'))

    return render_template('addplayer.html',
                           form=form, title='Dodawanie zawodnika')


@app.route('/teams/teams/edit<int:variable>')
def EditTeam(variable=None, methods=['POST', 'GET']):
    form = EditTeamForm()
    connection, cursor = polaczenie()
    Druzyny = pobierz_druzyny_do_edycji(connection, cursor, variable)
    if form.validate_on_submit():
        flash(
            'Drużyna została pomyślnie edytowana',
            'success')
        return redirect(url_for('match_history'))
    elif request.method == 'GET':
        form.TeamName.data = Druzyny[0]['nazwa']
        form.NumberOfPlayers.data = Druzyny[0]['Number_of_players']
        form.TeamManagerName.data = Druzyny[0]['Manager_name']
        form.TeamManagerSurname.data = Druzyny[0]['Manager_lastname']
    return render_template('editteam.html',
                           form=form, title='Edytowanie drużyny', posts=Druzyny,
                           variable=variable)


if __name__ == '__main__':
    app.run(debug=True)
