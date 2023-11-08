import datetime
import os

from babel import dates
from flask import Blueprint, abort, render_template, redirect, url_for, request, session

import bd
import utilitaires
from utilitaires import hacher_mdp

bp_compte = Blueprint('compte', __name__)


@bp_compte.route('/authentifier')
def page_de_connexion():
    return render_template('connexion.jinja', titre_page="CONNEXION", bouton_soumettre= "Connecter")


@bp_compte.route('/creer_compte', methods=["GET", "POST"])
def creation_de_compte():
    if request.method == "POST":
        courriel = (request.form.get("courriel", default=""))
        mdp = (request.form.get("mdp", default=""))
        courriel_valide = utilitaires.verifier_courriel(courriel)
        mdp_valide = utilitaires.verifier_mot_de_passe(mdp)
        if not courriel_valide or not mdp_valide:
            salut = "TODO"
        else:
            mdp_hacher = utilitaires.hacher_mdp(mdp)
            with bd.creer_connexion() as conn:
                bd.ajouter_utilisateur(conn, courriel, mdp)
    else:
        return render_template('connexion.jinja', titre_page="CRÉER COMPTE", bouton_soumettre="Créer le compte")



@bp_compte.route('/valider_authentifier', methods=['GET', 'POST'])
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