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


class NameNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class EmptyInput(Exception):
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


def get_club(email=None, name=None):
    """
    Recuperer les informations d'un club grâce à un email.
    Args:
        email(str): Email du club
    Raises:
        EmailNotFound: si aucun club trouvé
    Returns:
        dict: information du club
    """
    if email:
        for club in clubs:
            if email == club["email"]:
                return club
        raise EmailNotFound("Email du Club introuvable. Veuillez reessayer.")
    elif name:
        for club in clubs:
            if name == club["name"]:
                return club
        raise NameNotFound("Nom du Club introuvable. Veuillez reessayer.")
    else:
        raise EmptyInput('Veuillez remplir le formulaire.')


def get_competition(name):
    """
    Recuperer les informations d'une compétition grâce à un nom.
    Args:
        name(str): Nom de la compétition
    Raises:
        EmailNotFound: si aucune compétition trouvée
    Returns:
        dict: information de la compétition
    """
    for competition in competitions:
        if name == competition["name"]:
            return competition
    raise CompetitionNotFound("Compétition introuvable. Veuillez réessayer.")


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
        club = get_club(email=request.form["email"])
        return render_template(
            "welcome.html",
            club=club,
            competitions=competitions
        )
    except (EmailNotFound, EmptyInput) as e:
        return render_template('index.html', error=e.message), 404


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Affiche la page de réservation pour une compétition et un club spécifiques.

    Args:
        competition (str): Nom de la compétition
        club (str): Nom du club

    Retourne:
        str: Page de réservation ou page d'accueil
    """
    try:
        found_club = next(
            (c for c in clubs if c['name'] == club),
            None
        )
        found_competition = get_competition(competition)
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition
        )
    except (EmailNotFound, CompetitionNotFound) as e:
        return render_template(
            "index.html",
            error=e.message), 404


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    try:
        competition = get_competition(request.form['competition'])

        club = get_club(name=request.form['club'])
        placesRequired = int(request.form['places'])
    except (CompetitionNotFound, EmailNotFound) as e:
        return render_template('index.html', error=e.message), 400

    if placesRequired > int(competition['numberOfPlaces']):
        flash('Vous ne pouvez reserver plus que place que celle disponible.')
        return render_template(
            'welcome.html',
            club=club,
            competitions=competitions
            ), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Reservation Confirme')
    return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
