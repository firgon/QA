import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs() -> dict:
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def load_competitions() -> dict:
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


app = Flask(__name__)
app.config.from_object("config")

competitions = load_competitions()
clubs = load_clubs()


def get_club_with(criteria: str, value: str) -> dict:
    for club in clubs:
        if criteria in club.keys() and club[criteria] == value:
            return club
    else:
        return None


def get_competition_with(criteria: str, value: str) -> dict:
    for competition in competitions:
        if criteria in competition.keys() and competition[criteria] == value:
            return competition
    else:
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def show_summary():
    club = get_club_with('email', request.form['email'])
    if club is None:
        flash("You are not registered. You can't connect.")
        return redirect(url_for('index'))
    else:
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    found_club = get_club_with('name', club)
    found_competition = get_competition_with('name', competition)
    if found_club and found_competition:
        return render_template('booking.html', club=found_club,
                               competition=found_competition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club,
                               competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = get_competition_with('name', request.form['competition'])
    club = get_club_with('name', request.form['club'])
    places_required = int(request.form['places'])
    competition['numberOfPlaces'] = int(
        competition['numberOfPlaces']) - places_required
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
