import json
from flask import Flask, render_template, request, redirect, flash, url_for


def load_clubs():
    with open("clubs.json") as c:
        clubs = json.load(c)["clubs"]
        return clubs


def load_competitions():
    with open("competitions.json") as comps:
        competitions = json.load(comps)["competitions"]
        return competitions


app = Flask(__name__)
app.secret_key = "something_special"

competitions = load_competitions()
clubs = load_clubs()


class EmailNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class CompetitionNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def get_club(email):
    clubs = load_clubs()
    for club in clubs:
        if email == club["email"]:
            return club
    raise EmailNotFound("Club introuvables. Veuillez réessayer.")


def get_competition(name):
    competitions = load_competitions()
    for competition in competitions:
        if name == competition["name"]:
            return competition
    raise CompetitionNotFound("Compétition introuvables. Veuillez réessayer.")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    club = get_club(request.form["email"])
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template(
            "booking.html", club=foundClub, competition=foundCompetition
        )
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][
        0
    ]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
