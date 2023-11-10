import os

from babel import dates
from datetime import datetime
from flask import Blueprint, abort, render_template, redirect, url_for, request, session, flash
import re

import app
import bd

regex_paterne_titre = re.compile(r"([aA-zZ\s]{1,50})")
regex_paterne_description = re.compile(r"(^.{5,2000}$)")
regex_paterne_photo = re.compile(r"([\w*.-]{6,50})")

bp_objet = Blueprint('objet', __name__)

@bp_objet.route('/liste')
def page_liste_des_objets():
    """Gestion de l'affichage de tout les objets."""
    with bd.creer_connexion() as conn:
            objets = bd.obtenir_tous_les_objets(conn)
    return render_template('liste_des_objets.jinja', objets=objets)


@bp_objet.route('/ajouter', methods=["GET", "POST"])
def page_ajouter_un_objet():
    """Gestion de l'ajout et la modification d'un objet."""
    if session.get('courriel'):
        action = "/objet/ajouter"
        method = "POST"
        id = 0
        classe_titre = ""
        classe_description = ""
        nom_image = ""
        titre_form = "Ajouter un objet :"

        if request.method == "POST":
            titre = (request.form.get("titre", default="")).strip()
            description = (request.form.get("description", default="")).strip()
            categorie = request.form.get("categorie", default="")
            fichier = request.files['image']
            if not fichier:
                nom_image = "vide.jpg"
            else:
                nom_image = (str(datetime.now().timestamp()) + ".jpg")

            if not regex_paterne_titre.fullmatch(titre):
                classe_titre = "is-invalid"

            if not regex_paterne_description.fullmatch(description):
                classe_description = "is-invalid"

            if regex_paterne_titre.fullmatch(titre) and regex_paterne_description.fullmatch(
                    description) and regex_paterne_photo.fullmatch(nom_image):
                if nom_image != "vide.jpg":
                    chemin_complet = app.chemain_ajout(nom_image)
                    fichier.save(chemin_complet)

                src = app.attribuer_src(nom_image)

                with bd.creer_connexion() as conn:
                    bd.ajouter_un_objet(conn, titre, description, src, categorie, session.get('courriel'))

                with bd.creer_connexion() as conn:
                        id = bd.obtenir_id_dernier_objet_ajoute(conn)

                if id != None:
                    flash('Objet ajouté.')
                    return redirect("/", code=303)
                else:
                    pass
                #Todo message derreur
        else:
            titre = ""
            description = ""
            fichier = ""

        return render_template(
            'ajouter_et_editer_un_objet.jinja',
            titre=titre,
            description=description,
            classe_titre=classe_titre,
            classe_description=classe_description,
            fonction="Ajouter",
            action=action,
            method=method,
            titre_form=titre_form
        )
    else:
        abort(401)


@bp_objet.route('/confirmation')
def page_confirmation():
    """Gestion de la confimation d'une action. (POST-Redirect-GET)"""
    titre = request.args.get('titre', type=str)
    description = request.args.get('description', type=str)
    photo = request.args.get('photo', type=str)
    categorie = request.args.get('categorie', type=int)
    id = request.args.get('id', type=int)

    if not titre:
        abort(400, "Paramère 'nom' est manquant.")
    if not description:
        abort(400, "Paramère 'description' est manquant.")
    if not categorie:
        abort(400, "Paramère 'categorie' est manquant.")

        with bd.creer_connexion() as conn:
            objet = bd.obtenir_un_objet_par_id(conn, id)

    if objet['titre'] == titre and objet['description'] == description and objet["photo"] == photo and objet[
        "categorie"] == categorie:
        message = "L'opération a bien été effectuée.."
        classe = "bg-success"
    else:
        message = "L'opération n'a pas été effectuée."
        classe = "bg-danger"

    return render_template('confirmation.jinja', message=message, classe=classe)


@bp_objet.route('/details/<int:id>', methods=["GET"])
def page_details(id):
    """Gestion de page personnalisée d'un objet."""
    langue = request.args.get("langue", type=str)

    if langue == "fr":
        app.changer_langue("fr_CA")
    elif langue == "en":
        app.changer_langue("en_CA")

    with bd.creer_connexion() as conn:
        objet = bd.obtenir_un_objet_par_id(conn, id)

    date = app.format_date(objet['date'])

    return render_template('objet.jinja', objet=objet, date=date)


@bp_objet.route('/modifier/<int:id>', methods=["GET", "POST"])
def page_editer(id):
    """Gestion de la modification d'un objet."""
    method = "POST"
    classe_titre = ""
    classe_description = ""
    titre_form = "Modifier un objet :"

    if request.method == "POST":
        titre = (request.form.get("titre", default="")).strip()
        description = (request.form.get("description", default="")).strip()
        categorie = request.form.get("categorie", default="")
        fichier = request.files['image']
        if not fichier:
            nom_image = "vide.jpg"
        else:
            nom_image = (str(datetime.now().timestamp()) + ".jpg")
    else:
        titre = ""
        description = ""
        fichier = ""

    action = "/modifier?id=" + str(id)

    if request.method == "POST":

        if not regex_paterne_titre.fullmatch(titre):
            classe_titre = "is-invalid"

        if not regex_paterne_description.fullmatch(description):
            classe_description = "is-invalid"

        if regex_paterne_titre.fullmatch(titre) and regex_paterne_description.fullmatch(
                description) and regex_paterne_photo.fullmatch(nom_image):
            if nom_image != "vide.jpg":
                chemin_complet = os.path.join(
                    app.config['CHEMIN_VERS_AJOUTS'], nom_image
                )
                fichier.save(chemin_complet)

            src = "/" + app.config['ROUTE_VERS_AJOUTS'] + "/" + nom_image

            with bd.creer_connexion() as conn:
                bd.modifier_un_objet(conn, titre, description, src, categorie, id)

            return redirect(
                "/confirmation?titre=" + titre + "&description=" + description + "&photo=" + src + "&categorie=" + categorie + "&id=" + str(
                    id), code=303)

    with bd.creer_connexion() as conn:
        objet = bd.obtenir_un_objet_par_id(conn, id)

    titre = objet['titre']
    description = objet['description']
    categorie = objet['categorie']

    if not regex_paterne_titre.fullmatch(titre):
        classe_titre = "is-invalid"

    if not regex_paterne_description.fullmatch(description):
        classe_description = "is-invalid"

    if not titre:
        abort(400, "Paramère 'nom' est manquant.")
        # render_template(400)
    if not description:
        abort(400, "Paramère 'description' est manquant.")
    if not categorie:
        abort(400, "Paramère 'categorie' est manquant.")

    return render_template(
        'ajouter_et_editer_un_objet.jinja',
        titre=objet['titre'],
        description=objet['description'],
        classe_titre=classe_titre,
        classe_description=classe_description,
        fonction="Modifier",
        action=action,
        method=method,
        titre_form=titre_form
    )

@bp_objet.route('/troqueur/<int:id>', methods=["GET", "POST"])
def troquer(id):
    courriel = session.get('courriel')
    with bd.creer_connexion() as conn:
        objets = bd.obtenir_objets_utilisateur(conn, courriel)
    if objets is not None:
        return render_template('troqueur.jinja', objets=objets)
    else:
        return render_template('troqueur.jinja')

@bp_objet.route('/supprimer_objet/<int:id>', methods=["GET", "POST"])
def supprimer_objet(id):
    with bd.creer_connexion() as conn:
        bd.supprimer_objet(conn, id)
    flash("L'objet a bien été supprimé.")
    return redirect("/", code=303)