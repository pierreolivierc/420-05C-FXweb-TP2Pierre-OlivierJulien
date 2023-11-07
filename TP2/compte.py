
from flask import Blueprint, render_template, redirect, request, session

import bd
from utilitaires import hacher_mdp

bp_compte = Blueprint('compte', __name__)

@bp_compte.route('/authentifier', methods=['GET', 'POST'])
def authentifier():
    """Pour effectuer une authentification"""
    erreur = False
    courriel = request.form.get("courriel", default="")

    if (request.method == 'POST') :
        mdp = hacher_mdp(request.form.get("mdp"))
        # TODO modifier chercher_utilisateur et vérifier si conn is good
        conn = bd.creer_connexion()
        utilisateur = bd.chercher_utilisateur(conn)

#TODO corriger si pas erreur ou le faire directement dans bd.py?
    #return render_template(
        #'compte/authentifier.jinja',
        #courriel=courriel,
        #erreur=erreur
    #)

@bp_compte.route('/deconnecter')
def deconnexion():
    pass

@bp_compte.route('/creation_utilisateur')
def nouveau_utilisateur():
    return render_template('creation_utilisateur.jinja')

