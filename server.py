import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)


class EmailNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class CompetitionNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def load_clubs():
    """
    Charge les clubs à partir d'un fichier JSON.
    Retourne:
        List[dict]: Liste des clubs.
    """
    with open("clubs.json") as c:
        clubs = json.load(c)["clubs"]
        return clubs


def load_competitions():
    """
    Charge les compétitions à partir d'un fichier JSON.
    Retourne:
        List[dict]: Liste des compétitions.
    """
    with open("competitions.json") as comps:
        competitions = json.load(comps)["competitions"]
        return competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


def get_club(email):
    clubs = load_clubs()
    for club in clubs:
        if email == club["email"]:
            return club
    raise EmailNotFound("Club introuvables. Veuillez reessayer.")


def get_competition(name):
    competitions = load_competitions()
    for competition in competitions:
        if name == competition["name"]:
            return competition
    raise CompetitionNotFound("Compétition introuvables. Veuillez réessayer.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/show_summary", methods=["POST"])
def show_summary():
    """
    Gère la connexion du club via email.

    Valide l'email soumis et affiche la page de bienvenue si valide.

    Retourne:
        str: Page de bienvenue rendue ou message d'erreur
    """
    try:
        club = get_club(request.form["email"])
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )
    except EmailNotFound as e:
        return render_template('index.html', error=e.message), 401


@app.route("/book/<competition>/<club>")
def book(competition, club):
    found_club = get_club(request.form["email"])
    found_competition = get_competition(request.form("name"))
    if found_club and found_competition:
        return render_template(
            "booking.html", club=club, competition=found_competition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )


@app.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    club = get_club(request.form["email"])
    competition = get_competition(request.form("name"))
    places_required = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
    flash("Great-booking complete!")
    return render_template(
        "welcome.html",
        club=club,
        competitions=competitions
    )


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
