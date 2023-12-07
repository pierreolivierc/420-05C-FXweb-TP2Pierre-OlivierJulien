"use strict";

async function supprimer_rester(){
    var resultat = await envoyerRequeteAjax('/comptes/liste_utilisateur', "GET", null, null);
    if(resultat['success'] === true){
        document.getElementById(resultat['courriel']).hidden
    }

}
function initialisation() {
    var tousLesBoutons = document.querySelectorAll('.bouton_supprimer');
    for(let i = 0; i < tousLesBoutons; i++){
        tousLesBoutons[i].addEventListener("click", supprimer_rester);
    }

}

window.addEventListener("load", initialisation);