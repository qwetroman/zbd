from flask import Flask, render_template, flash, redirect, url_for, request
from forms import (AddTeamForm, AddGameForm, AddStadionForm, AddPlayerForm,
                   EditTeamForm, AddSeasonForm, EditSquadForm, EditPlayerForm, TransferForm, DeleteStadionForm)
from baza import (polaczenie, odlacz, pobierz_druzyny, pobierz_zawodnikow,
                  pobierz_druzyny_do_edycji, pobierz_sklad, pobierz_sezony,
                  pobierz_gracza, pobierz_sezon, pobierz_stadiony, pobierz_stadion, update_stadium, create_stadium, delete_stadium)
# import mysql.connector
# from mysql.connector import Error

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e185681a407ace961e0bf2fdcdced1c7'

History = [
    {
        'team1': 'temp',
        'team2': 'temp',
        'team1_score': 'temp',
        'team2_score': 'temp',
        'data_gry': 'temp2',
        'stadion': 'nasd'
    }
]

Trenerzy = [
    {
        'name': 'cokolwiek',
        'last_name': 'temp',
        'phone': 'temp2',
        'nationality': 'poland',
        'team_name': 'Lech'
    }
]


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/teams', methods=['GET', 'POST'])
def about():
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
    connection, cursor = polaczenie()
    Stadiony = pobierz_stadiony(connection, cursor)
    print(Stadiony)
    return render_template('stadions.html', title='Stadiony',
                           posts=Stadiony)


@app.route('/players')
def players():
    connection, cursor = polaczenie()
    Gracze = pobierz_zawodnikow(connection, cursor)
    odlacz(cursor, connection)
    return render_template('players.html', title="Gracze", posts=Gracze)


@app.route('/coaches')
def coaches():
    trenerzy = Trenerzy
    return render_template('coaches.html', title="Trenerzy", posts=trenerzy)


@app.route('/seasons', methods=['GET', 'POST'])
def seasons():
    connection, cursor = polaczenie()
    sezony = pobierz_sezony(connection, cursor)
    return render_template('seasons.html', title='Sezony', posts=sezony)


@app.route('/AddTeam', methods=['GET', 'POST'])
def AddTeam():
    form = AddTeamForm()
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
        create_stadium(form.adres.data,
                       form.seats.data, form.nazwa.data)
        return redirect(url_for('stadions'))

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


@app.route('/seasons/add', methods=['GET', 'POST'])
def AddSeason():
    form = AddSeasonForm()
    if form.validate_on_submit():
        flash(
            'Sezon został pomyślnie dodany',
            'success')
        return redirect(url_for('home'))
    return render_template('addseason.html',
                           form=form, title='Dodawanie stadionu')


@app.route('/teams/edit/<int:variable>', methods=['GET', 'POST'])
def EditTeam(variable):
    form = EditTeamForm()
    connection, cursor = polaczenie()
    Druzyny = pobierz_druzyny_do_edycji(connection, cursor, variable)
    if form.validate_on_submit():
        flash(
            'Drużyna została pomyślnie edytowana',
            'success')
        return redirect(url_for('about'))
    elif request.method == 'GET':
        form.TeamName.data = Druzyny[0]['nazwa']
        form.NumberOfPlayers.data = Druzyny[0]['Number_of_players']
        form.TeamManagerName.data = Druzyny[0]['Manager_name']
        form.TeamManagerSurname.data = Druzyny[0]['Manager_lastname']
    return render_template('editteam.html',
                           form=form, title='Edytowanie drużyny',
                           posts=Druzyny, variable=variable)


@app.route('/teams/squad/edit/<int:variable>', methods=['GET', 'POST'])
def EditSquad(variable):
    connection, cursor = polaczenie()
    Druzyny = pobierz_sklad(connection, cursor, variable)
    form = EditSquadForm()
    if form.validate_on_submit():
        flash(
            'Drużyna została pomyślnie edytowana',
            'success')
        return redirect(url_for('SeeTeam', variable))
    elif request.method == 'GET':
        form.name1.data = Druzyny[0]['name']
        form.last_name1.data = Druzyny[0]['last_name']
        form.phone1.data = Druzyny[0]['phone_number']

    return render_template('editsquad.html',
                           title=f'Edycja {Druzyny[0]["team_name"]}',
                           posts=Druzyny, variable=variable, form=form)


@app.route('/players/edit/<int:variable>', methods=['GET', 'POST'])
def EditPlayer(variable):
    connection, cursor = polaczenie()
    gracz = pobierz_gracza(connection, cursor, variable)
    form = EditPlayerForm()
    if form.validate_on_submit():
        flash(
            'Gracz został pomyślnie edytowany',
            'success')
        return redirect(url_for('players', variable))
    elif request.method == 'GET':
        form.name.data = gracz[0]['name']
        form.last_name.data = gracz[0]['last_name']
        form.phone.data = gracz[0]['phone_number']

    return render_template('editplayer.html',
                           title=f'Edycja {gracz[0]["name"]}',
                           posts=gracz, variable=variable, form=form)


@app.route('/match_history/edit/<int:variable>', methods=['GET', 'POST'])
def EditGame(variable):
    connection, cursor = polaczenie()
    gracz = pobierz_gracza(connection, cursor, variable)
    form = EditPlayerForm()
    if form.validate_on_submit():
        flash(
            'Gracz został pomyślnie edytowany',
            'success')
        return redirect(url_for('players', variable))
    elif request.method == 'GET':
        form.name.data = gracz[0]['name']
        form.last_name.data = gracz[0]['last_name']
        form.phone.data = gracz[0]['phone_number']

    return render_template('editplayer.html',
                           title=f'Edycja {gracz[0]["name"]}',
                           posts=gracz, variable=variable, form=form)


@app.route('/seasons/edit/<int:variable>', methods=['GET', 'POST'])
def EditSeason(variable):
    connection, cursor = polaczenie()
    sezon = pobierz_sezon(connection, cursor, variable)
    form = AddSeasonForm()
    if form.validate_on_submit():
        flash(
            'Sezon został pomyślnie edytowany',
            'success')
        return redirect(url_for('seasons', variable))
    elif request.method == 'GET':
        form.name.data = sezon[0]['name']
        form.country.data = sezon[0]['country']
        form.beggining.data = sezon[0]['beggining']
        form.end.data = sezon[0]['end']

    return render_template('editseason.html',
                           title=f'Edycja {sezon[0]["name"]}',
                           posts=sezon, variable=variable, form=form)


@app.route('/stadions/edit/<int:variable>', methods=['GET', 'POST'])
def EditStadion(variable):
    connection, cursor = polaczenie()
    stadion = pobierz_stadion(connection, cursor, variable)
    form = AddStadionForm()
    if form.validate_on_submit():
        flash(
            'Stadion został pomyślnie edytowany',
            'success')
        update_stadium(connection, cursor, variable,
                       form.adres.data, form.seats.data, form.nazwa.data)
        return redirect(url_for('stadions'))
    elif request.method == 'GET':
        form.nazwa.data = stadion[0]['name']
        form.adres.data = stadion[0]['address']
        form.seats.data = stadion[0]['capacity']
    return render_template('add_stadion.html',
                           posts=stadion, variable=variable, form=form)


@app.route('/stadions/delete/<int:variable>', methods=['GET', 'POST'])
def DeleteStadion(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        flash(
            'Stadion został pomyślnie usunięty',
            'success')
        delete_stadium(variable)
        return redirect(url_for('stadions'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/teams/see<int:variable>', methods=['GET', 'POST'])
def SeeTeam(variable=None):
    connection, cursor = polaczenie()
    Druzyny = pobierz_sklad(connection, cursor, variable)
    return render_template('seeteam.html',
                           title=f'Skład {Druzyny[0]["team_name"]}',
                           posts=Druzyny, variable=variable)


@app.route('/teams/transfer<int:variable>', methods=['GET', 'POST'])
def TransferPlayer(variable):
    form = TransferForm()
    if form.validate_on_submit():
        flash(
            'Gracz został pomyślnie przeniesiony')
        return redirect(url_for('SeeTeam', variable=variable))
    return render_template("transfer.html", variable=variable, form=form)


if __name__ == '__main__':
    app.run(debug=True)
