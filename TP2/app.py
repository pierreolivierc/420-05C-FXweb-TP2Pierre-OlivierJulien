from flask import Flask, render_template, request, redirect, abort
# from flask_babel import Babel
from babel import numbers, dates
from datetime import datetime

import os
import bd
import re

app = Flask(__name__)

app.config["BABEL_DEFAULT_LOCALE"] = "fr_CA"

regex_paterne_titre = re.compile(r"([aA-zZ\s]{1,50})")
regex_paterne_description = re.compile(r"(^.{5,2000}$)")
regex_paterne_photo = re.compile(r"([\w*.-]{6,50})")

app.config['MORCEAUX_VERS_AJOUTS'] = ["static", "images", "ajouts"]

app.config['ROUTE_VERS_AJOUTS'] = "/".join(app.config['MORCEAUX_VERS_AJOUTS'])

app.config['CHEMIN_VERS_AJOUTS'] = os.path.join(
    app.instance_path.replace("instance", ""),
    *app.config['MORCEAUX_VERS_AJOUTS']
)


@app.route('/accueil')
def page_accuiel():
    """Gestion de la page d'accuil."""
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT * FROM `objets` ORDER BY date DESC LIMIT 5;')
            objets = curseur.fetchall()
    return render_template('index.jinja', objets=objets)


@app.route('/liste des objets')
def page_liste_des_objets():
    """Gestion de l'affichage de tout les objets."""
    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute('SELECT * FROM `objets` ORDER BY id DESC;')
            objets = curseur.fetchall()
    return render_template('index.jinja', objets=objets)


@app.route('/ajouter un objet', methods=["GET", "POST"])
def page_ajouter_un_objet():
    """Gestion de l'ajout et la modification d'un objet."""
    action = "/ajouter un objet"
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

    else:
        titre = ""
        description = ""
        fichier = ""

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
            with bd.creer_connexion() as connexion:
                with connexion.get_curseur() as curseur:
                    curseur.execute(
                        'INSERT INTO `objets` (`id`, `titre`, `description`, `photo`, `categorie`, `date`) VALUES (NULL, %(titre)s, %(description)s, %(image)s, %(categorie)s, CURRENT_DATE);',
                        {
                            'titre': titre,
                            'description': description,
                            'image': src,
                            'categorie': categorie
                        }
                    )
            with bd.creer_connexion() as connexion:
                with connexion.get_curseur() as curseur:
                    curseur.execute('SELECT `id` FROM `objets` ORDER BY id DESC LIMIT 1')
                    id = curseur.fetchone()
            return redirect(
                "/confirmation?titre=" + titre + "&description=" + description + "&photo=" + src + "&categorie=" + categorie + "&id=" + str(
                    id['id']), code=303)

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


@app.route('/confirmation')
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

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute(
                'SELECT * FROM `objets` WHERE id = %(id)s',
                {
                    'id': id
                }
            )
            objet = curseur.fetchone()
    if objet['titre'] == titre and objet['description'] == description and objet["photo"] == photo and objet[
        "categorie"] == categorie:
        message = "L'opération a bien été effectuée.."
        classe = "bg-success"
    else:
        message = "L'opération n'a pas été effectuée."
        classe = "bg-danger"

    return render_template('confirmation.jinja', message=message, classe=classe)


@app.route('/details', methods=["GET"])
def page_details():
    """Gestion de page personnalisée d'un objet."""
    identifiant = request.args.get("id", type=int)
    langue = request.args.get("langue", type=str)

    if langue == "fr":
        app.config["BABEL_DEFAULT_LOCALE"] = "fr_CA"
    elif langue == "en":
        app.config["BABEL_DEFAULT_LOCALE"] = "en_CA"


    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute(
                'SELECT * FROM `objets` WHERE id = %(id)s;',
                {
                    'id': identifiant
                }
            )
            objet = curseur.fetchone()
    date = dates.format_date(objet['date'], locale=app.config["BABEL_DEFAULT_LOCALE"])

    return render_template('objet.jinja', objet=objet, date=date, )


@app.route('/modifier', methods=["GET", "POST"])
def page_editer():
    """Gestion de la modification d'un objet."""
    method = "POST"
    classe_titre = ""
    id = ""
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

    id = request.args.get("id", type=int)

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
            with bd.creer_connexion() as connexion:
                with connexion.get_curseur() as curseur:
                    curseur.execute(
                        'UPDATE `objets` SET `titre` = %(titre)s, `description` = %(description)s, `photo` = %(image)s, `categorie` = %(categorie)s WHERE `objets`.`id` = %(id)s;',
                        {
                            'titre': titre,
                            'description': description,
                            'image': src,
                            'categorie': categorie,
                            'id': id
                        }
                    )
            return redirect(
                "/confirmation?titre=" + titre + "&description=" + description + "&photo=" + src + "&categorie=" + categorie + "&id=" + str(
                    id), code=303)

    with bd.creer_connexion() as connexion:
        with connexion.get_curseur() as curseur:
            curseur.execute(
                'SELECT * FROM `objets` WHERE id = %(id)s;',
                {
                    'id': id
                }
            )
            objet = curseur.fetchone()

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


@app.errorhandler(400)
def mauvaise_requete(e):
    """Gestion de l'erreur 400"""
    erreur = e.description
    return render_template('erreur.jinja', message="Un paramètre du formulaire est manquant", erreur=erreur), 400


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
