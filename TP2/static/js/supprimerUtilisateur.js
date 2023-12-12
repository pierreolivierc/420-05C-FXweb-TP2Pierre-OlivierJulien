"use strict";

async function supprimer_rester(event){
    event.preventDefault();

    // Récupérer le courriel à partir de l'attribut data-courriel
    var courriel = event.currentTarget.getAttribute('data-courriel');
    var resultat = await envoyerRequeteAjax('/comptes/liste_utilisateur', "POST", {courriel: courriel}, null);

    if (resultat['success'] === true) {
        document.getElementById(resultat['courriel']).style.display = 'none';
    }

}
function initialisation() {
    var tousLesBoutons = document.getElementsByClassName('bouton_supprimer');
    for (let i = 0; i < tousLesBoutons.length; i++) {
        tousLesBoutons[i].addEventListener("click", supprimer_rester);
    }
}


window.addEventListener("load", initialisation);