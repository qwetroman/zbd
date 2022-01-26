from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, NoneOf
from baza import pobierz_nazwy_druzyn, pobierz_zawodnikow_i_numery, pobierz_wolnego_managera, pobierz_stadiony, pobierz_wolnych_zawodnikow


class AddTeamForm(FlaskForm):

    TeamName = StringField('Nazwa drużyny', [
                           DataRequired(), Length(min=2)])

    Player1 = SelectField('Zawodnik 1',
                          validators=[DataRequired()])
    Player2 = SelectField('Zawodnik 2',
                          validators=[DataRequired()])
    Player3 = SelectField('Zawodnik 3',
                          validators=[DataRequired()])
    Player4 = SelectField('Zawodnik 4',
                          validators=[DataRequired()])
    Player5 = SelectField('Zawodnik 5',
                          validators=[DataRequired()])
    Player6 = SelectField('Zawodnik 6',
                          validators=[DataRequired()])
    Player7 = SelectField('Zawodnik 7',
                          validators=[DataRequired()])
    Player8 = SelectField('Zawodnik 8',
                          validators=[DataRequired()])
    Player9 = SelectField('Zawodnik 9',
                          validators=[DataRequired()])
    Player10 = SelectField('Zawodnik 10',
                           validators=[DataRequired()])
    Player11 = SelectField('Zawodnik 11',
                           validators=[DataRequired()])

    StadionName = SelectField(
        'Nazwa stadionu domowego', validators=[DataRequired()])

    TeamManagerName = SelectField(
        'Wybierz wolnego menadżera', validators=[DataRequired()])

    BudgetBalance = IntegerField(
        'Stan budżetu drużyny', [DataRequired()])

    BudgetDept = IntegerField(
        'Dług drużyny', [Optional()])

    BudgetProfit = IntegerField(
        'Zysk drużyny', [DataRequired()])

    BudgetExpenses = IntegerField(
        'Wydatki drużyny', [DataRequired()])

    submit = SubmitField("Dodaj drużynę")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        seen = set()
        for field in [self.Player1, self.Player2, self.Player3, self.Player4, self.Player5, self.Player6, self.Player7, self.Player8, self.Player9, self.Player10, self.Player11]:
            if field.data in seen:
                field.errors.append('Please select three distinct choices.')
                result = False
            else:
                seen.add(field.data)
        return result


class AddGameForm(FlaskForm):

    TeamO = SelectField(u'Drużyna 1',
                        validators=[DataRequired()])
    TeamT = SelectField(u'Drużyna 2',
                        validators=[DataRequired()])
    PointsO = IntegerField("Punkty drużyny 1", [DataRequired()])
    PointsT = IntegerField("Punkty drużyny 2", [DataRequired()])
    StadionName = SelectField(
        "Nazwa stadionu", [DataRequired(), Length(min=2)])
    GameDate = DateField(
        "Data gry", [DataRequired()])
    submit = SubmitField("Dodaj grę")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        seen = set()
        for field in [self.TeamO, self.TeamT]:
            if field.data in seen:
                field.errors.append('Please select three distinct choices.')
                result = False
            else:
                seen.add(field.data)
        return result


class AddStadionForm(FlaskForm):
    nazwa = StringField("Nazwa stadionu", [DataRequired()])
    adres = StringField("Adres stadionu", [DataRequired()])
    seats = IntegerField(
        'Ilośc siedzeń', [DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Zatwierdź")


class DeleteStadionForm(FlaskForm):
    submit = SubmitField("Usuń")


class AddPlayerForm(FlaskForm):
    # teams = pobierz_nazwy_druzyn()
    # teams.append('Brak drużyny')
    name = StringField("Imię gracza", [DataRequired()])
    lastname = StringField("Nazwisko gracza", [DataRequired()])
    phone = StringField("Phone number", [DataRequired()])
    # team = SelectField("Drużyna (opcjonalne)", choices=teams,
    #                    validators=[DataRequired()])
    submit = SubmitField("Dodaj zawodnika")


class EditPlayerForm(FlaskForm):
    name = StringField("Imię gracza", [DataRequired()])
    last_name = StringField("Nazwisko gracza", [DataRequired()])
    phone = StringField("Phone number", [DataRequired()])
    submit = SubmitField("Edytuj zawodnika")


class AddSeasonForm(FlaskForm):
    name = StringField("Nazwa sezonu", [DataRequired()])
    country = StringField("Kraj", [DataRequired()])
    beggining = DateField("Początek", [DataRequired()])
    end = DateField("Koniec", [DataRequired()])
    submit = SubmitField("Edytuj sezon")


class EditTeamForm(FlaskForm):
    TeamName = StringField('Nazwa drużyny', [
        Length(min=2)])

    NumberOfPlayers = IntegerField('Liczba graczy',
                                   [NumberRange(min=11, max=23,
                                                message='Minimum number of'
                                                + 'players is 11, max 23')])

    StadionName = StringField('Nazwa stadionu domowego')

    TeamManagerName = StringField(
        'Imię menadżera')

    TeamManagerSurname = StringField(
        'Nazwisko menadżera')

    BudgetBalance = IntegerField(
        'Stan budżetu drużyny')

    BudgetDept = IntegerField(
        'Dług drużyny', [Optional()])

    BudgetProfit = IntegerField(
        'Zysk drużyny')

    BudgetExpenses = IntegerField(
        'Wydatki drużyny')

    submit = SubmitField("Edytuj drużynę")


class TransferForm(FlaskForm):
    Druzyny = SelectField("Drużyna do ktorej gracz zostanie przeniesiony",
                          validators=[DataRequired()])
    Koszt = IntegerField("Koszt transferu", [
                         DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Dokonaj transferu")


class EditSquadForm(FlaskForm):
    Zawodnik = SelectField("Wolni gracze",
                           validators=[DataRequired()])
    submit = SubmitField("Dodaj zawodnika")


class AddPhysioForm(FlaskForm):
    players = pobierz_zawodnikow_i_numery()
    name = StringField('Imię', [DataRequired()])
    last_name = StringField('Nazwisko', [DataRequired()])
    type = StringField('Typ', [DataRequired()])
    phone = StringField('Numer telefonu', [DataRequired()])

    player = SelectField("Zawodnik", choices=players,
                         validators=[DataRequired()])
    submit = SubmitField("Zatwierdź")


class AddCoachForm(FlaskForm):

    name = StringField('Imię', [DataRequired()])
    last_name = StringField('Nazwisko', [DataRequired()])
    phone = StringField('Numer telefonu', [DataRequired()])
    nationality = StringField('Narodowośc', [DataRequired()])

    team = SelectField("Druzyna",
                       validators=[DataRequired()])
    submit = SubmitField("Dodaj")


class AddManagerForm(FlaskForm):
    name = StringField('Imię', [DataRequired()])
    last_name = StringField('Nazwisko', [DataRequired()])
    phone = StringField('Numer telefonu', [DataRequired()])
    submit = SubmitField("Dodaj")
