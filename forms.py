from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, DateField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class AddTeamForm(FlaskForm):
    TeamName = StringField('Nazwa drużyny', [
                           DataRequired(), Length(min=2)])

    NumberOfPlayers = IntegerField('Liczba graczy',
                                   [DataRequired(),
                                    NumberRange(min=11, max=23,
                                                message='Minimum number of'
                                                + 'players is 11, max 23')])

    StadionName = StringField('Nazwa stadionu domowego', [DataRequired()])

    TeamManagerName = StringField(
        'Imię menadżera', [DataRequired()])

    TeamManagerSurname = StringField(
        'Nazwisko menadżera', [DataRequired()])

    BudgetBalance = IntegerField(
        'Stan budżetu drużyny', [DataRequired()])

    BudgetDept = IntegerField(
        'Dług drużyny', [Optional()])

    BudgetProfit = IntegerField(
        'Zysk drużyny', [DataRequired()])

    BudgetExpenses = IntegerField(
        'Wydatki drużyny', [DataRequired()])

    submit = SubmitField("Dodaj drużynę")


class AddGameForm(FlaskForm):
    TeamO = StringField("Nazwa druzyny 1", [DataRequired(), Length(min=2)])
    TeamT = StringField("Nazwa druzyny 2", [DataRequired(), Length(min=2)])
    StadionName = StringField(
        "Nazwa stadionu", [DataRequired(), Length(min=2)])
    GameDate = DateField(
        "Data gry", [DataRequired()])
    submit = SubmitField("Dodaj grę")


class AddStadionForm(FlaskForm):
    nazwa = StringField("Nazwa stadionu", [DataRequired()])
    adres = StringField("Adres stadionu", [DataRequired()])
    seats = IntegerField(
        'Ilośc siedzeń', [DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Dodaj stadion")


class AddPlayerForm(FlaskForm):
    name = StringField("Imię gracza", [DataRequired()])
    lastname = StringField("Nazwisko gracza", [DataRequired()])
    phone = StringField("Phone number", [DataRequired()])
    team = StringField("Drużyna (opcjonalne)")
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
    submit = SubmitField("Dodaj stadion")


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


class EditSquadForm(FlaskForm):
    name1 = StringField("Imię zawodnika", [DataRequired()])
    last_name1 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone1 = StringField("Numer telefonu", [DataRequired()])

    name2 = StringField("Imię zawodnika", [DataRequired()])
    last_name2 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone2 = StringField("Numer telefonu", [DataRequired()])

    name3 = StringField("Imię zawodnika", [DataRequired()])
    last_name3 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone3 = StringField("Numer telefonu", [DataRequired()])

    name4 = StringField("Imię zawodnika", [DataRequired()])
    last_name4 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone4 = StringField("Numer telefonu", [DataRequired()])

    name5 = StringField("Imię zawodnika", [DataRequired()])
    last_name5 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone5 = StringField("Numer telefonu", [DataRequired()])

    name6 = StringField("Imię zawodnika", [DataRequired()])
    last_name6 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone6 = StringField("Numer telefonu", [DataRequired()])

    name7 = StringField("Imię zawodnika", [DataRequired()])
    last_name7 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone7 = StringField("Numer telefonu", [DataRequired()])

    name8 = StringField("Imię zawodnika", [DataRequired()])
    last_name8 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone8 = StringField("Numer telefonu", [DataRequired()])

    name9 = StringField("Imię zawodnika", [DataRequired()])
    last_name9 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone9 = StringField("Numer telefonu", [DataRequired()])

    name10 = StringField("Imię zawodnika", [DataRequired()])
    last_name10 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone10 = StringField("Numer telefonu", [DataRequired()])

    name11 = StringField("Imię zawodnika", [DataRequired()])
    last_name11 = StringField("Nazwisko zawodnika", [DataRequired()])
    phone11 = StringField("Numer telefonu", [DataRequired()])

    name11 = StringField("Imię zawodnika")
    last_name11 = StringField("Nazwisko zawodnika")
    phone11 = StringField("Numer telefonu")

    name12 = StringField("Imię zawodnika")
    last_name12 = StringField("Nazwisko zawodnika")
    phone12 = StringField("Numer telefonu")

    name13 = StringField("Imię zawodnika")
    last_name13 = StringField("Nazwisko zawodnika")
    phone13 = StringField("Numer telefonu")

    name14 = StringField("Imię zawodnika")
    last_name14 = StringField("Nazwisko zawodnika")
    phone14 = StringField("Numer telefonu")

    name15 = StringField("Imię zawodnika")
    last_name15 = StringField("Nazwisko zawodnika")
    phone15 = StringField("Numer telefonu")

    name16 = StringField("Imię zawodnika")
    last_name16 = StringField("Nazwisko zawodnika")
    phone16 = StringField("Numer telefonu")

    name17 = StringField("Imię zawodnika")
    last_name17 = StringField("Nazwisko zawodnika")
    phone17 = StringField("Numer telefonu")

    name18 = StringField("Imię zawodnika")
    last_name18 = StringField("Nazwisko zawodnika")
    phone18 = StringField("Numer telefonu")

    name19 = StringField("Imię zawodnika")
    last_name19 = StringField("Nazwisko zawodnika")
    phone19 = StringField("Numer telefonu")

    name20 = StringField("Imię zawodnika")
    last_name20 = StringField("Nazwisko zawodnika")
    phone20 = StringField("Numer telefonu")

    name21 = StringField("Imię zawodnika")
    last_name21 = StringField("Nazwisko zawodnika")
    phone21 = StringField("Numer telefonu")

    name22 = StringField("Imię zawodnika")
    last_name22 = StringField("Nazwisko zawodnika")
    phone22 = StringField("Numer telefonu")

    name23 = StringField("Imię zawodnika")
    last_name23 = StringField("Nazwisko zawodnika")
    phone23 = StringField("Numer telefonu")

    submit = SubmitField("Edytuj skład")
