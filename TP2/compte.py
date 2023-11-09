import datetime
import hashlib
import os

from babel import dates
from flask import Blueprint, abort, render_template, redirect, url_for, request, session, flash

import bd
import utilitaires
from utilitaires import hacher_mdp

bp_compte = Blueprint('compte', __name__)

@bp_compte.route('/authentifier', methods=["GET", "POST"])
def page_de_connexion():
    if (request.method == 'POST') :
        courriel = (request.form.get("courriel", default=""))
        mdp = (request.form.get("mdp", default=""))
        mdphacher = utilitaires.hacher_mdp(mdp)
        with bd.creer_connexion() as conn:
            utilisateur = bd.chercher_utilisateur(conn, courriel, mdphacher)
        if utilisateur != None:
            creer_session(courriel)
            flash('Connexion réussi.')
            return redirect("/", code=303)
        else:
            return render_template('connexion.jinja', titre_page="CONNEXION", blueprint="authentifier", bouton_soumettre="Connecter")
    else:
        return render_template('connexion.jinja', titre_page="CONNEXION", blueprint="authentifier", bouton_soumettre= "Connecter")


@bp_compte.route('/creer_compte', methods=["GET", "POST"])
def creation_de_compte():
    if request.method == "POST":
        courriel = (request.form.get("courriel", default=""))
        mdp = (request.form.get("mdp", default=""))
        courriel_valide = utilitaires.verifier_courriel(courriel)
        mdp_valide = utilitaires.verifier_mot_de_passe(mdp)
        with bd.creer_connexion() as conn:
            Courriel = bd.verifier_si_courriel_existe(conn, courriel)
        if not courriel_valide or not mdp_valide or Courriel :
            # TODO ajout d'une condition en cas d'erreur
            salut = "TODO"
            flash('Erreur.')
            return redirect("/", code=303)
        else:
            mdp = utilitaires.hacher_mdp(mdp)

            with bd.creer_connexion() as conn:
                bd.ajouter_utilisateur(conn, courriel, mdp)

            with bd.creer_connexion() as conn:
              utilisateur = bd.chercher_utilisateur(conn,courriel, mdp)

            if utilisateur != None:
                creer_session(courriel)
                flash('Compte bien créé.')
                return redirect("/", code=303)
            else:
                return render_template('connexion.jinja', titre_page="CRÉER COMPTE", blueprint="creer_compte", bouton_soumettre="Créer le compte")
    else:
        return render_template('connexion.jinja', titre_page="CRÉER COMPTE", blueprint="creer_compte", bouton_soumettre="Créer le compte")


#@bp_compte.route('/valider_authentifier', methods=['GET', 'POST'])
#def authentifier():
#    """Pour effectuer une authentification"""
#    erreur = False
#     if (request.method == 'POST') :
#        courriel = (request.form.get("courriel", default=""))
#        mdp = (request.form.get("mdp", default=""))
#        mdphacher = utilitaires.hacher_mdp(mdp)
#        with bd.creer_connexion() as conn:
#            utilisateur = bd.chercher_utilisateur(conn, courriel, mdphacher)
#        if utilisateur != None:
#            creer_session(courriel)
#            flash('Connexion réussi.')
#            return redirect("/", code=303)
#        else:
#            pass


#TODO corriger si pas erreur ou le faire directement dans bd.py?
    #return render_template(
        #'compte/authentifier.jinja',
        #courriel=courriel,
        #erreur=erreur
    #)


@bp_compte.route('/deconnecter')
def deconnexion():
    """Permet à l'utilisateur de se deconnecter"""
    session.clear()
    flash('Déconnection réussi.')
    return redirect("/", code=303)


def creer_session(courriel):
    if session:
        session.clear()
    session.permanent = True
    session['courriel'] = courriel