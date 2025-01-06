import json
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    flash,
    url_for
)
from datetime import datetime


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
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_club(email=None, name=None):
    """
    Recuperer les informations d'un club grâce à un email.
    Args:
        email(str): Email du club
    Raises:
        EmailNotFound: si aucun club trouvé
        NameNotFound: si aucun club trouvé
        EmptyInput: si aucun email de club est fourni
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
            competitions=competitions,
            current_time=current_time
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
        found_club = get_club(name=club)
        found_competition = get_competition(competition)
        return render_template(
            "booking.html",
            club=found_club,
            competition=found_competition,
            current_time=current_time
        )
    except (CompetitionNotFound, NameNotFound) as e:
        return render_template(
            "index.html",
            error=e.message), 404


@app.route('/purchase_places', methods=['POST'])
def purchase_places():
    try:
        competition = get_competition(request.form['competition'])
        club = get_club(name=request.form['club'])
        placesRequired = int(request.form['places'])
    except (CompetitionNotFound, NameNotFound, ValueError) as e:
        return render_template('index.html', error=e.message), 400
    errors = data_validation(competition, club, placesRequired)
    if errors:
        for error in errors:
            flash(error, 'error')
        return render_template(
            'booking.html',
            competition=competition,
            club=club,
            current_time=current_time
        ), 400

    competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
    club['points'] = int(club['points']) - placesRequired
    flash('Réservation confirmée !')
    return render_template(
        'welcome.html',
        club=club,
        competitions=competitions,
        current_time=current_time
    )


def data_validation(competition, club, placesRequired):
    """Valide les données pour l'achat de places."""
    errors = []
    competition_date = datetime.strptime(
        competition['date'], '%Y-%m-%d %H:%M:%S'
    )
    if competition_date < datetime.now():
        errors.append(
            'Vous ne pouvez réserver des places pour des compétitions passée.'
        )

    if placesRequired > int(competition['numberOfPlaces']):
        errors.append(
            'Vous ne pouvez réserver plus de places que celles disponibles.'
        )

    if placesRequired > 12:
        errors.append(
            'Vous ne pouvez réserver plus de 12 places sur une compétition.'
        )

    if placesRequired > int(club['points']):
        errors.append(
            'Vous ne pouvez réserver plus de places que vos points disponibles.'
        )
    if placesRequired < 0:
        errors.append(
            'Vous ne pouvez réserver 0 places.'
        )

    return errors

# TODO: Add route for points display


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
