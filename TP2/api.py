from flask import Blueprint, abort, request, session, jsonify
import bd

bp_api = Blueprint('api', __name__)


@bp_api.route('/recherche')
def recherche():
    """Recherche"""
    mots_cles = request.args.get("mots-cles")

    with bd.creer_connexion() as conn:
        recherche = bd.recherche_objet_par_input(conn, mots_cles)
    return jsonify(recherche)

@bp_api.route('/accueil_asynchrone')
def accueil_asynchrone():
    """Retourne les 5 derniers objets aux 5 secondes"""
    with bd.creer_connexion() as conn:
        objet = bd.obtenir_les_premier_objets(conn)
    return jsonify(objet)

@bp_api.route('/information_utilisateur')
def information_utilisateur():
    """Retourne un dictionnaire comportant les informations utilisateurs"""
    if 'courriel' in session:
        courriel = str(session['courriel'])
        return jsonify(courriel)
    else:
        return "Aucune information de courriel dans la session"


@bp_api.route('/information_administateur')
def information_administrateur():
    """Retourne un dictionnaire comportant les informations utilisateurs"""
    if 'admin' in session:
        admin = str(session['admin'])
        return jsonify(admin)
    else:
        return "Aucune information d'administrateur dans la session"


@bp_api.route('/les_recherches')
def les_recherches():
    """Retourne les recherches de l'utilisateur"""
    if session.get('courriel'):
        liste_de_recherche = session.get('recherches', [])
        return jsonify(liste_de_recherche)
    else:
        abort(401)

@bp_api.route('/les_quatres_suivants')
def les_quatres_suivants():
    """Retourne les quatres objets suivants"""
    mots_cles = request.args.get("mot-cle")
    index = request.args.get("index")
    with bd.creer_connexion() as conn:
        objets = bd.obtenir_objets_par_recherche(conn, mots_cles, index)
    return jsonify(objets)
