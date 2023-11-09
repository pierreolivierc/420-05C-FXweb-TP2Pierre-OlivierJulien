from flask import Flask, render_template, request, redirect, abort
# from flask_babel import Babel
from babel import numbers, dates
from datetime import datetime

import os
import bd
import re

from compte import bp_compte
from objet import bp_objet

app = Flask(__name__)

app.config["BABEL_DEFAULT_LOCALE"] = "fr_CA"

regex_paterne_titre = re.compile(r"([aA-zZ\s]{1,50})")
regex_paterne_description = re.compile(r"(^.{5,2000}$)")
regex_paterne_photo = re.compile(r"([\w*.-]{6,50})")

app.config['MORCEAUX_VERS_AJOUTS'] = ["static", "images", "ajouts"]

app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])

app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(
    app.instance_path.replace("instance", ""),
    *app.config['MORCEAUX_VERS_AJOUTS'])

app.register_blueprint(bp_objet, url_prefix='/objet')
app.register_blueprint(bp_compte, url_prefix='/compte')

app.secret_key = 'b51213b260450a05dc8d0619a1e6850dd2e6902c0dcc9b02369749761b4b5f2f'


@app.route('/')
def page_accueil():
    """Gestion de la page d'accuil."""
    with bd.creer_connexion() as conn:
            objets = bd.obtenir_les_premier_objets(conn)
    return render_template('index.jinja', objets=objets)


@app.errorhandler(400)
def mauvaise_requete(e):
    """Gestion de l'erreur 400"""
    erreur = e.description
    return render_template('erreur.jinja', message="Un paramètre du formulaire est manquant", erreur=erreur), 400


@app.errorhandler(401)
def mauvaise_requete(e):
    """Gestion de l'erreur 400"""
    erreur = e.description
    return render_template('erreur.jinja', message="Vous n'êtes pas authentifié.", erreur=erreur), 400


@app.errorhandler(403)
def mauvaise_requete(e):
    """Gestion de l'erreur 403"""
    erreur = e.description
    return render_template('erreur.jinja', message="Vous n'avez pas l'autorisation pour accéder à cette page", erreur=erreur), 400

@app.errorhandler(404)
def mauvaise_requete(e):
    """Gestion de l'erreur 404"""
    erreur = e.description
    return render_template('erreur.jinja', message="Page inexistante.", erreur=erreur), 404


@app.errorhandler(500)
def mauvaise_requete(e):
    """Gestion de l'erreur 500"""
    erreur = e.description
    return render_template('erreur.jinja', message="Une erreur est survenue en lien avec la base de données.",
                           erreur=erreur), 500


def changer_langue(langue):
    app.config["BABEL_DEFAULT_LOCALE"] = langue

def chemain_ajout(nom_image):
    return  os.path.join(
        app.config['CHEMIN_VERS_AJOUTS'], nom_image
    )

def attribuer_src(nom_image):
   return "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image

def format_date(date):
    date = dates.format_date(date, locale=app.config["BABEL_DEFAULT_LOCALE"])
    return date