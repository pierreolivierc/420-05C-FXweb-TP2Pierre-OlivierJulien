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
