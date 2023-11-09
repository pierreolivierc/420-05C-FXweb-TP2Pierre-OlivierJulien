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
    if (request.method == 'POST'):
        courriel = (request.form.get("courriel", default=""))
        mdp = (request.form.get("mdp", default=""))
        mdphacher = utilitaires.hacher_mdp(mdp)
        with bd.creer_connexion() as conn:
            utilisateur = bd.chercher_utilisateur(conn, courriel, mdphacher)
        if utilisateur != None:
            creer_session(courriel, utilisateur['admin'])
            flash('Connexion réussi.')
            return redirect("/", code=303)
        else:
            flash('Erreur: Le courriel ou le mot de passe est invalide.')
            return render_template('connexion.jinja')
    else:
        return render_template('connexion.jinja')


@bp_compte.route('/creer_compte', methods=["GET", "POST"])
def creation_de_compte():
    if request.method == "POST":
        courriel = (request.form.get("courriel", default=""))
        mdp = (request.form.get("mdp", default=""))
        mdp2 = (request.form.get("mdp2", default=""))
        courriel_valide = utilitaires.verifier_courriel(courriel)
        mdp_valide = utilitaires.verifier_mot_de_passe(mdp)
        with bd.creer_connexion() as conn:
            Courriel = bd.verifier_si_courriel_existe(conn, courriel)
        if not courriel_valide or not mdp_valide or Courriel or mdp != mdp2:
            # TODO ajout d'une condition en cas d'erreur
            if not courriel_valide or Courriel:
                flash('Erreur: Courriel invalide.')
            elif not mdp_valide:
                flash(
                    'Le mot de passe doit respecter les règles suivantes : Une lettre majuscule, une lettre minuscule, un nombre et avoir une longueur de 8 charactères au minimum')
            elif mdp != mdp2:
                flash('Erreur : Les deux mots de passe ne sont pas identiques.')
            else:
                flash('Erreur.')

            return render_template('creation_utilisateur.jinja')
        else:
            mdp = utilitaires.hacher_mdp(mdp)

            with bd.creer_connexion() as conn:
                bd.ajouter_utilisateur(conn, courriel, mdp)

            with bd.creer_connexion() as conn:
                utilisateur = bd.chercher_utilisateur(conn, courriel, mdp)

            if utilisateur != None:
                creer_session(courriel, utilisateur['admin'])
                flash('Compte bien créé.')
                return redirect("/", code=303)
            else:
                return render_template('creation_utilisateur.jinja')
    else:
        return render_template('creation_utilisateur.jinja')


# @bp_compte.route('/valider_authentifier', methods=['GET', 'POST'])
# def authentifier():
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


# TODO corriger si pas erreur ou le faire directement dans bd.py?
# return render_template(
# 'compte/authentifier.jinja',
# courriel=courriel,
# erreur=erreur
# )

def creer_session(courriel, admin):
    if session:
        session.clear()
    session.permanent = True
    session['courriel'] = courriel
    session['admin'] = admin


@bp_compte.route('/deconnecter')
def deconnexion():
    """Permet à l'utilisateur de se deconnecter"""
    session.clear()
    flash('Déconnection réussi.')
    return redirect("/", code=303)


@bp_compte.route('/liste_utilisateur', methods=["GET", "POST"])
def lister_utilisateur():
    admin = session.get('admin')
    if admin == 1:
        if (request.method == 'POST'):
            courriel = (request.form.get("courriel", default=""))
            with bd.creer_connexion() as conn:
                bd.supprimer_utilisateur(conn, courriel)
                tous_les_utilisateurs = bd.obtenir_tous_les_utilisateur(conn)
                flash("Utilisateur "+courriel+" a été supprimé.")
            return render_template('/liste_utilisateur.jinja', utilisateur=tous_les_utilisateurs)
        else:
            with bd.creer_connexion() as conn:
                tous_les_utilisateurs = bd.obtenir_tous_les_utilisateur(conn)
            return render_template('/liste_utilisateur.jinja', utilisateur=tous_les_utilisateurs)
    elif admin == 0:
        abort(403)
    else:
        abort(401)
