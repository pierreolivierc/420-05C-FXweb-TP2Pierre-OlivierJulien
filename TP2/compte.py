import datetime
import os

from babel import dates
from flask import Blueprint, abort, render_template, redirect, url_for, request, session
import re

import app
import bd

bp_compte = Blueprint('compte', __name__)

@bp_compte.route('/authentifier')
def page_de_connexion():
    return render_template('connexion.jinja')

@bp_compte.route('/deconnecter')
def deconnexion():
    pass

@bp_compte.route('/creation_utilisateur')
def nouveau_utilisateur():
    return render_template('creation_utilisateur.jinja')