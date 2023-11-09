"""Connexion a la bd"""

import types
import contextlib
import mysql.connector


@contextlib.contextmanager
def creer_connexion():
    """Pour créer une connexion à la BD"""
    conn = mysql.connector.connect(
        user="garneau",
        password="qwerty123",
        host="127.0.0.1",
        database="tp1web3",
        raise_on_warnings=True
    )

    # Pour ajouter la méthode getCurseur() à l'objet connexion
    conn.get_curseur = types.MethodType(get_curseur, conn)

    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    else:
        conn.commit()
    finally:
        conn.close()


@contextlib.contextmanager
def get_curseur(self):
    """Permet d'avoir *tous* les enregistrements dans un dictionnaire"""
    curseur = self.cursor(dictionary=True, buffered=True)
    try:
        yield curseur
    finally:
        curseur.close()


def obtenir_les_premier_objets(conn):
    """Retourne les cinq dernier objets ajoutés"""
    with conn.get_curseur() as curseur:
        curseur.execute('SELECT * FROM `objets` ORDER BY date DESC LIMIT 5;')
        return curseur.fetchall()


def obtenir_tous_les_objets(conn):
    """Retourne tous les objets"""
    with conn.get_curseur() as curseur:
        curseur.execute('SELECT * FROM `objets` ORDER BY id DESC;')
        return curseur.fetchall()


def ajouter_un_objet(conn, titre, description, src, categorie, courriel):
    """Ajouter un nouvel objet"""
    with conn.get_curseur() as curseur:
        curseur.execute(
            'INSERT INTO `objets` (`id`, `titre`, `description`, `photo`, `categorie`, `date`, `Proprietaire`) VALUES (NULL, %(titre)s, %(description)s, %(image)s, %(categorie)s, CURRENT_DATE, %(courriel)s);',
            {
                'titre': titre,
                'description': description,
                'image': src,
                'categorie': categorie,
                'courriel': courriel
            }
        )


def ajouter_utilisateur(conn, courriel, mdp):
    with conn.get_curseur() as curseur:
        curseur.execute(
            'INSERT INTO utilisateur (courriel, mdp, admin) VALUES (%(courriel)s, %(mdp)s, 0)',
            {
                'courriel': courriel,
                'mdp': mdp
            }
        )


def verifier_si_courriel_existe(conn, courriel):
    with conn.get_curseur() as curseur:
        curseur.execute(
            'SELECT utilisateur.courriel FROM utilisateur WHERE utilisateur.courriel = %(courriel)s;',
            {
                'courriel': courriel,
            }
        )
        return curseur.fetchone()


def chercher_utilisateur(conn, courriel, mdp):
    with conn.get_curseur() as curseur:
        curseur.execute('SELECT * FROM utilisateur WHERE courriel = %s AND mdp = %s', (courriel, mdp))
        utilisateur = curseur.fetchone()
        erreur = (utilisateur is None)
        if not erreur:
            return utilisateur
        else:
            salut ="todo"
    # TODO gestion d'une erreur en cas que l'utilisateur existe pas, voir exercice 9


def obtenir_id_dernier_objet_ajoute(conn):
        with conn.get_curseur() as curseur:
            curseur.execute('SELECT `id` FROM `objets` ORDER BY id DESC LIMIT 1')
            return curseur.fetchone()


def obtenir_un_objet_par_id(conn, id):
        with conn.get_curseur() as curseur:
            curseur.execute(
                'SELECT * FROM `objets` WHERE id = %(id)s',
                {
                    'id': id
                }
            )
            return curseur.fetchone()


def obtenir_tous_les_utilisateur(conn):
    with conn.get_curseur() as curseur:
        curseur.execute('SELECT * FROM `utilisateur`')
        return curseur.fetchall()


def modifier_un_objet(conn, titre, description, src, categorie, id):
        with conn.get_curseur() as curseur:
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


def supprimer_utilisateur(conn, courriel):
    with conn.get_curseur() as curseur:
        curseur.execute(
            'DELETE FROM `utilisateur` WHERE `courriel` = %(courriel)s;',
            {
                'courriel': courriel,
            }
        )
