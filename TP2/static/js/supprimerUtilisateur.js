"use strict";

async function suprimer_relister(){
    var resultat = await envoyerRequeteAjax('/comptes/liste_utilisateur', "GET", null, null);
    if(resultat['success'] === true){
        
    }

}
function initialisation() {
    document.addEventListener(suprimer_relister());
}

window.addEventListener("load", initialisation);