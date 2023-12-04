import datetime
import hashlib
import os

from babel import dates
from flask import Blueprint, abort, render_template, redirect, url_for, request, session, flash

import bd
import utilitaires
from utilitaires import hacher_mdp

bp_api = Blueprint('api', __name__)


@bp_api.route('/recherche')
def recherche():
    """Recherche"""
    mots_cles = request.args.get("mots-cles")

    with bd.creer_connexion() as conn:
        recherche = bd.recherche_objet_par_input(conn, mots_cles)
    return recherche

@bp_api.route('/accueil_asynchrone')
def accueil_asynchrone():
    """Retourne les 5 derniers objets aux 5 secondes"""

    with bd.creer_connexion() as conn:
        objet = bd.obtenir_les_premier_objets_asynchrone(conn)
    return objet


@bp_api.route('/supprimer_utilisateur')
def supprimer_utilisateur():
    """Supprimer un utilisateur"""

    with bd.creer_connexion() as conn:
        bd.supprimer_utilisateur(conn,)
