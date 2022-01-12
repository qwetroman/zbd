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
