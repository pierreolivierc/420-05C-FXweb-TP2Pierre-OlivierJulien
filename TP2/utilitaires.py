
import hashlib, re

def hacher_mdp(mdp_en_clair):
    """Prend un mot de passe en clair et lui applique une fonction de hachage"""
    return hashlib.sha512(mdp_en_clair.encode('utf-8')).hexdigest()


def verifier_mot_de_passe(mot_de_passe):
    if re.match(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$", mot_de_passe):
        return True
    else:
        return False


def verifier_courriel(courriel):
    if re.match(r"^[a-zA-Z0-9._]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$", courriel):
        return True
    else:
        return False

