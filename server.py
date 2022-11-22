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
MAX_BOOKING = 12


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


def check_is_correct_required_places(required_places, club, competition) \
        -> (bool, str):
    """function to check if required places is :
    upper than 0 (you can't book 0 place or less)
    less than or equal to maximum authorised (12)
    less than or equal to remaining place in competition
    less than or equal to remaining point of the club
    @:param required_places: int
    @:param club: dict with club infos

    @:return boolean is correct or not
    @:return message, to explain"""

    if required_places <= 0:
        return False, "You can't book 0 or less places !"

    if required_places > int(club['points']):
        return False, f"You don't have enough points" \
                      f" to book {required_places} places !"

    if required_places > MAX_BOOKING:
        return False, f"You can't book more than {MAX_BOOKING} places !"

    if required_places > int(competition['numberOfPlaces']):
        return False, f"You can't book {required_places} places," \
                      f"because {competition['name']} has only " \
                      f"{competition['numberOfPlaces']} places remaining."

    return True, 'Great-booking complete!'


@app.route('/purchasePlaces', methods=['POST'])
def purchase_places():
    competition = get_competition_with('name', request.form['competition'])
    club = get_club_with('name', request.form['club'])
    required_places = int(request.form['places'])
    is_correct, message = check_is_correct_required_places(required_places,
                                                           club,
                                                           competition)
    flash(message)

    if is_correct:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) \
                                        - required_places
        club['points'] = int(club['points']) - required_places

    return render_template('welcome.html', club=club,
                           competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
