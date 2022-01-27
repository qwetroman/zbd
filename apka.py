from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import (AddTeamForm, AddGameForm, AddStadionForm, AddPlayerForm,
                   EditTeamForm, AddSeasonForm, EditSquadForm, EditPlayerForm,
                   TransferForm, DeleteStadionForm, AddPhysioForm,
                   AddCoachForm, AddManagerForm)
from baza import (polaczenie, odlacz, pobierz_druzyny, pobierz_zawodnikow,
                  pobierz_druzyny_do_edycji, pobierz_sklad, pobierz_sezony,
                  pobierz_gracza, pobierz_sezon, pobierz_stadiony, pobierz_stadion,
                  update_stadium, create_stadium, delete_stadium,
                  pobierz_managera, pobierz_physio_id, pobierz_fizio,
                  create_physio, delete_physio, pobierz_coach, create_coach,
                  delete_coach, update_physios, create_manager, add_player, create_player, pobierz_nazwy_druzyn, pobierz_wolnych_zawodnikow, pobierz_wolnego_managera, pobierz_stadiony_team)
# import mysql.connector
# from mysql.connector import Error
import baza
import forms
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

Fizjo = [
    {
        'name': 'cokolwiek',
        'last_name': 'temp',
        'phone': 'temp2',
        'type': 'normal',
        'player_name': 'Lech',
        'player_last_name': 'Nowak'
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


@app.route('/physios', methods=['GET', 'POST'])
def Physios():
    posts = pobierz_fizio()

    return render_template('physios.html', title='Fizjoterapeuci', posts=posts)


@app.route('/physios/add', methods=['GET', 'POST'])
def PhysiosAdd():
    form = AddPhysioForm()
    if request.method == 'POST':
        flash(
            'Fizjoterapeuta zostal pomyslnie edytowany',
            'success')
        create_physio(form.name.data, form.last_name.data,
                      form.phone.data, form.type.data, form.player.data)
        return redirect(url_for('Physios'))

    return render_template('addphysio.html',
                           form=form, title='Dodawanie fizjoterapeuty')


@app.route('/physios/edit/<int:variable>', methods=['GET', 'POST'])
def EditPhysios(variable):
    form = AddPhysioForm()
    physio = pobierz_physio_id(variable)
    if request.method == 'POST':
        flash(
            'Fizjoterapeuta zostal pomyslnie edytowany',
            'success')
        name, last_name, number = form.player.data.split()
        update_physios(variable, form.name.data, form.last_name.data,
                       form.phone.data, form.type.data, name, last_name, number)
        return redirect(url_for('Physios'))
    elif request.method == 'GET':
        form.name.data = physio[0]['name']
        form.last_name.data = physio[0]['last_name']
        form.type.data = physio[0]['type']
        form.phone.data = physio[0]['phone']

    return render_template('editphysio.html',
                           form=form, title='Edytowanie fizjoterapeuty', variable=variable)


@app.route('/physios/delete/<int:variable>', methods=['GET', 'POST'])
def DeletePhysio(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        flash(
            'Fizjoterapeuta został pomyślnie usunięty',
            'success')
        delete_physio(variable)
        return redirect(url_for('Physios'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/match_history')
def match_history():
    connection, cursor = polaczenie()
    History = baza.pobierz_historie(connection, cursor)
    return render_template('match_history.html', title='Historia gier',
                           posts=History)


@app.route('/manager')
def manager():
    posts = pobierz_managera()
    return render_template('managers.html', title='Menadżerzy', posts=posts)


@app.route('/manager/create', methods=['GET', 'POST'])
def AddManager():
    form = AddManagerForm()
    if form.validate_on_submit():
        flash(
            'Trener zostal pomyslnie dodany',
            'success')
        create_manager(form.name.data, form.last_name.data,
                       form.phone.data)
        return redirect(url_for('manager'))

    return render_template('addmanager.html',
                           form=form, title='Dodawanie trenera')


@app.route('/manager/edit/<int:variable>', methods=['GET', 'POST'])
def EditManager(variable):
    form = forms.EditManagerForm()
    connection, cursor = polaczenie()
    if form.validate_on_submit():
        flash(
            'Trener zostal pomyslnie dodany',
            'success')
        baza.update_manager(connection, cursor, variable, form.name.data, form.last_name.data,
                            form.phone.data)
        return redirect(url_for('manager'))

    return render_template('editmanager.html',
                           form=form, title='Edytowanie managera', variable=variable)


@app.route('/stadions')
def stadions():
    connection, cursor = polaczenie()
    Stadiony = pobierz_stadiony(connection, cursor)
    odlacz(cursor, connection)
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
    trenerzy = pobierz_coach()
    return render_template('coaches.html', title="Trenerzy", posts=trenerzy)


@app.route('/coaches/add', methods=['GET', 'POST'])
def AddCoach():
    form = AddCoachForm()
    connection, cursor = polaczenie()
    druzyny = pobierz_nazwy_druzyn(connection, cursor)
    form.team.choices = druzyny
    if form.validate_on_submit():
        flash(
            'Trener zostal pomyslnie dodany',
            'success')
        create_coach(form.name.data, form.last_name.data,
                     form.phone.data, form.nationality.data, int(form.team.data.split()[-1]))
        return redirect(url_for('coaches'))
    odlacz(connection, cursor)
    return render_template('addcoach.html',
                           form=form, title='Dodawanie trenera')


@app.route('/coaches/delete/<int:variable>', methods=['GET', 'POST'])
def DeleteCoach(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        flash(
            'Trener został pomyślnie usunięty',
            'success')
        delete_coach(variable)
        return redirect(url_for('coaches'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/seasons', methods=['GET', 'POST'])
def seasons():
    connection, cursor = polaczenie()
    sezony = pobierz_sezony(connection, cursor)
    return render_template('seasons.html', title='Sezony', posts=sezony)


@app.route('/teams/edit/<int:variable>', methods=['GET', 'POST'])
def EditTeam(variable):
    form = EditTeamForm()
    connection, cursor = polaczenie()
    nazwy = pobierz_nazwy_druzyn(connection, cursor)
    cursor.execute("SELECT team_menager.first_name,team_menager.last_name,team_menager.manager_id from team_menager inner join football_team on football_team.manager_id = team_menager.manager_id where football_team.team_id=%s", (int(variable),))
    man = cursor.fetchall()
    man = man[0][0] + " " + man[0][1] + " " + str(man[0][2])
    cursor.execute("SELECT stadion.name,stadion.stadion_id from stadion inner join football_team on football_team.stadion_id = stadion.stadion_id where football_team.team_id=%s", (int(variable),))
    stad = cursor.fetchall()
    stad = stad[0][0] + " " + str(stad[0][1])
    stadiony = []
    zawodnicy = []
    menagerzy = []
    menagerzy.append(man)
    stadiony.append(stad)
    sezony = []
    for x in baza.pobierz_wolne_stadiony(connection, cursor):
        stadiony.append(x['name'] + " " + str(x['id']))
    for x in pobierz_sezony(connection, cursor):
        sezony.append(x['name'] + " " + str(x['id']))
    for x in pobierz_wolnych_zawodnikow(connection, cursor):
        zawodnicy.append(x['name'] + " " + x['last_name'] + " " + str(x['id']))
    for x in pobierz_wolnego_managera(connection, cursor):
        menagerzy.append(x['Name'] + " " + x['Surname'] + " " + str(x['id']))
    form.TeamName.NoneOf = nazwy
    form.StadionName.choices = stadiony
    form.TeamManagerName.choices = menagerzy
    form.SeasonName.choices = sezony
    if form.validate_on_submit():
        baza.update_team(connection, cursor, variable, request.form['TeamName'], int(request.form['StadionName'].split()[-1]), int(request.form['SeasonName'].split()[-1]), int(
            request.form['TeamManagerName'].split()[-1]), int(request.form['BudgetBalance']), int(request.form['BudgetDept']), int(request.form['BudgetProfit']), int(request.form['BudgetExpenses']))
        connection.commit()
        odlacz(connection, cursor)
        flash(
            'Drużyna została pomyślnie edytowana',
            'success')
        return redirect(url_for('about'))
    return render_template('editteam.html',
                           form=form, title='Edytowanie drużyny',
                           variable=variable)


@app.route('/AddTeam', methods=['GET', 'POST'])
def AddTeam():
    form = AddTeamForm()
    connection, cursor = polaczenie()
    nazwy = pobierz_nazwy_druzyn(connection, cursor)
    stadiony = []
    zawodnicy = []
    menagerzy = []
    sezony = []
    for x in baza.pobierz_wolne_stadiony(connection, cursor):
        stadiony.append(x['name'] + " " + str(x['id']))
    for x in pobierz_sezony(connection, cursor):
        sezony.append(x['name'] + " " + str(x['id']))
    for x in pobierz_wolnych_zawodnikow(connection, cursor):
        zawodnicy.append(x['name'] + " " + x['last_name'] + " " + str(x['id']))
    for x in pobierz_wolnego_managera(connection, cursor):
        menagerzy.append(x['Name'] + " " + x['Surname'] + " " + str(x['id']))
    form.Player1.choices = zawodnicy
    form.Player2.choices = zawodnicy
    form.Player3.choices = zawodnicy
    form.Player4.choices = zawodnicy
    form.Player5.choices = zawodnicy
    form.Player6.choices = zawodnicy
    form.Player7.choices = zawodnicy
    form.Player8.choices = zawodnicy
    form.Player9.choices = zawodnicy
    form.Player10.choices = zawodnicy
    form.Player11.choices = zawodnicy
    form.TeamName.NoneOf = nazwy
    form.StadionName.choices = stadiony
    form.TeamManagerName.choices = menagerzy
    form.SeasonName.choices = sezony

    if form.validate_on_submit():
        print((request.form['TeamName'], int(request.form['StadionName'].split()[-1]), int(request.form['SeasonName'].split()[-1]), int(request.form['TeamManagerName'].split()[-1]), int(request.form['BudgetBalance']), int(request.form['BudgetDept']), int(request.form['BudgetProfit']), int(request.form['BudgetExpenses']), int(request.form['Player1'].split()[-1]), int(request.form['Player2'].split(
        )[-1]), int(request.form['Player3'].split()[-1]), int(request.form['Player4'].split()[-1]), int(request.form['Player5'].split()[-1]), int(request.form['Player6'].split()[-1]), int(request.form['Player7'].split()[-1]), int(request.form['Player8'].split()[-1]), int(request.form['Player9'].split()[-1]), int(request.form['Player10'].split()[-1]), int(request.form['Player11'].split()[-1]))
        )
        baza.add_team(connection, cursor, request.form['TeamName'], int(request.form['StadionName'].split()[-1]), int(request.form['SeasonName'].split()[-1]), int(request.form['TeamManagerName'].split()[-1]), int(request.form['BudgetBalance']), int(request.form['BudgetDept']), int(request.form['BudgetProfit']), int(request.form['BudgetExpenses']), int(request.form['Player1'].split()[-1]), int(request.form['Player2'].split(
        )[-1]), int(request.form['Player3'].split()[-1]), int(request.form['Player4'].split()[-1]), int(request.form['Player5'].split()[-1]), int(request.form['Player6'].split()[-1]), int(request.form['Player7'].split()[-1]), int(request.form['Player8'].split()[-1]), int(request.form['Player9'].split()[-1]), int(request.form['Player10'].split()[-1]), int(request.form['Player11'].split()[-1]))

        flash(
            'Druzyna została pomyślnie dodana',
            'success')
        return redirect(url_for('coaches'))
    return render_template('addteam.html',
                           form=form, title='Dodawanie druzyny')


@app.route('/add_game', methods=['GET', 'POST'])
def AddGame():
    form = AddGameForm()
    connection, cursor = polaczenie()
    teams = pobierz_nazwy_druzyn(connection, cursor)
    stadiony = pobierz_stadiony_team(connection, cursor)
    form.TeamO.choices = teams
    form.TeamT.choices = teams
    form.StadionName.choices = stadiony
    if form.validate_on_submit():
        idO = form.TeamO.data.split()
        idT = form.TeamT.data.split()
        # request.form['Koszt'])
        flash(
            'Gra zostala pomyslnie dodana',
            'success')
        baza.create_history(connection, cursor, idO[-1], idT[-1], request.form['PointsO'],
                            request.form['PointsT'], request.form['GameDate'], request.form['StadionName'])
        odlacz(connection, cursor)
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
        connection, cursor = polaczenie()
        flash(
            'Zawodnik został pomyślnie dodany',
            'success')
        create_player(connection, cursor, form.name.data,
                      form.lastname.data, form.phone.data)
        odlacz(connection, cursor)
        return redirect(url_for('players'))

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


@app.route('/teams/squad/edit/<int:variable>', methods=['GET', 'POST'])
def EditSquad(variable):
    connection, cursor = polaczenie()
    form = forms.EditSquadForm()
    connection, cursor = polaczenie()
    zawodnicy = []
    for x in pobierz_wolnych_zawodnikow(connection, cursor):
        zawodnicy.append(x['name'] + " " + x['last_name']
                         + " " + str(x['id']))
    form.Zawodnik.choices = zawodnicy
    if form.validate_on_submit():
        id = form.Zawodnik.data.split()
        if baza.add_to_team(connection, cursor, id[-1], variable) == -1:
            flash("Sklad liczy wiecej niz 23 zawodnikow")
            return redirect(url_for('SeeTeam', variable=variable))
        else:
            flash(
                'Zawodnik został pomyślnie dodany',
                'success')
            return redirect(url_for('SeeTeam', variable=variable))

    return render_template('editsquad.html', variable=variable, form=form)


@app.route('/players/edit/<int:variable>', methods=['GET', 'POST'])
def EditPlayer(variable):
    connection, cursor = polaczenie()
    gracz = pobierz_gracza(connection, cursor, variable)
    form = EditPlayerForm()
    if form.validate_on_submit():
        baza.update_player(connection, cursor, variable,
                           form.name.data, form.last_name.data, form.phone.data)
        flash(
            'Gracz został pomyślnie edytowany',
            'success')
        return redirect(url_for('players', variable=variable))
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


@app.route('/match_hisotry/edit/<int:variable>', methods=['GET', 'POST'])
def DeleteGame(variable):
    connection, cursor = polaczenie()
    form = DeleteStadionForm()
    if form.validate_on_submit():
        try:
            baza.delete_history(connection, cursor, variable)
            flash(
                'Gra została pomyślnie usunięta',
                'success')
            odlacz(connection, cursor)
            return redirect(url_for('match_history'))
        except:
            flash("Drużyna w bazie, błąd")
            return redirect(url_for('match_history'))

    odlacz(connection, cursor)
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/seasons/edit/<int:variable>', methods=['GET', 'POST'])
def EditSeason(variable):
    connection, cursor = polaczenie()
    sezon = pobierz_sezon(connection, cursor, variable)
    form = AddSeasonForm()
    if form.validate_on_submit():
        flash(
            'Sezon został pomyślnie edytowany',
            'success')
        return redirect(url_for('seasons', variable=variable))
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
        try:
            delete_stadium(variable)
            flash(
                'Stadion został pomyślnie usunięty',
                'success')
            return redirect(url_for('stadions'))
        except:
            flash("Błąd. Stadion domowy drużyny")
            return redirect(url_for('stadions'))

    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/seasons/delete/<int:variable>', methods=['GET', 'POST'])
def DeleteSeason(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        connection, cursor = polaczenie()
        # try:
        baza.delete_season(connection, cursor, variable)
        flash(
            'Stadion został pomyślnie usunięty',
            'success')
        odlacz(connection, cursor)
        return redirect(url_for('seasons'))
        # except:
        #     flash("Błąd. Stadion domowy drużyny")
        #     odlacz(connection, cursor)
        #     return redirect(url_for('seasons'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/players/delete/<int:variable>', methods=['GET', 'POST'])
def DeletePlayer(variable):
    connection, cursor = polaczenie()
    form = DeleteStadionForm()
    if form.validate_on_submit():
        if baza.delete_player(connection, cursor, variable) == 0:
            flash(
                'Gracz został pomyślnie usunięty',
                'success')
            odlacz(connection, cursor)
            return redirect(url_for('players'))
        else:
            flash('Cannot remove player from that team')
            return redirect(url_for('players'))
    odlacz(connection, cursor)
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/teams/delete/<int:variable>', methods=['GET', 'POST'])
def DeleteTeam(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        connection, cursor = polaczenie()
        flash(
            'Druzyna została pomyślnie usunięta',
            'success')
        baza.delete_team(connection, cursor, variable)
        odlacz(connection, cursor)
        return redirect(url_for('about'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/teams/see<int:variable>', methods=['GET', 'POST'])
def SeeTeam(variable=None):
    connection, cursor = polaczenie()
    Druzyny = pobierz_sklad(connection, cursor, variable)
    if len(Druzyny) > 0:
        session['team_id_to_transfer'] = Druzyny[0]['id']
    return render_template('seeteam.html',
                           title='Sklad',
                           posts=Druzyny, variable=variable)


@app.route('/teams/transfer<int:player_id>', methods=['GET', 'POST'])
def TransferPlayer(player_id):
    connection, cursor = polaczenie()
    teams = pobierz_nazwy_druzyn(connection, cursor)
    teams.append("Wyrzuc")
    form = TransferForm()
    form.Druzyny.choices = teams
    if form.validate_on_submit():
        if form.Druzyny.data != "Wyrzuc":
            out = form.Druzyny.data.split()
            if baza.transfer_player(connection, cursor, player_id, session.get('team_id_to_transfer', None), out[-1], request.form['Koszt']) == 0:
                flash(
                    'Gracz został pomyślnie przeniesiony')
                odlacz(connection, cursor)
                return redirect(url_for('SeeTeam', variable=session.get('team_id_to_transfer', None)))
            else:
                flash('Error')
                odlacz(connection, cursor)
                return redirect(url_for('SeeTeam', variable=session.get('team_id_to_transfer', None)))
        else:
            baza.free_player(connection, cursor, player_id)
            odlacz(connection, cursor)
            return redirect(url_for('SeeTeam', variable=session.get('team_id_to_transfer', None)))
    odlacz(connection, cursor)
    return render_template("transfer.html", form=form, player_id=player_id)


@app.route('/employees', methods=['GET', 'POST'])
def Employees():
    connection, cursor = polaczenie()
    pracownicy = baza.pobierz_employee(connection, cursor)
    odlacz(connection, cursor)
    return render_template("employees.html", posts=pracownicy)


@app.route('/employees/add', methods=['GET', 'POST'])
def AddEmployee():
    form = forms.AddEmployeeForm()
    connection, cursor = polaczenie()
    teams = pobierz_nazwy_druzyn(connection, cursor)
    form.team.choices = teams
    if form.validate_on_submit():
        flash(
            'Pracownik został pomyślnie dodany',
            'success')
        baza.create_employee(connection, cursor, form.name.data, form.last_name.data, form.phone.data, int(
            request.form['team'].split()[-1]), form.receptionist.data)
        return redirect(url_for('Employees'))
    return render_template("addemployee.html", form=form)


@app.route('/employees/delete/<int:variable>', methods=['GET', 'POST'])
def DeleteEmployee(variable):
    form = DeleteStadionForm()
    if form.validate_on_submit():
        connection, cursor = polaczenie()
        flash(
            'Pracownik został pomyślnie usunięty',
            'success')
        baza.delete_employee(connection, cursor, variable)
        odlacz(connection, cursor)
        return redirect(url_for('Employees'))
    return render_template('delete_stadion.html', variable=variable, form=form)


@app.route('/employees/edit/<int:variable>', methods=['GET', 'POST'])
def EditEmployee(variable):
    form = forms.EditEmployeeForm()
    connection, cursor = polaczenie()
    # teams = pobierz_nazwy_druzyn(connection, cursor)
    # form.team.choices = teams
    if form.validate_on_submit():
        flash(
            'Pracownik został pomyślnie edytowany',
            'success')
        baza.update_employee(connection, cursor, form.name.data,
                             form.last_name.data, form.phone.data, variable)
        return redirect(url_for('Employees'))
    return render_template("editemployee.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
