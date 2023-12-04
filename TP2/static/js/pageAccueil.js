"use strict";

async function accueil_au_5_seconde(){
    console.log('Accueil au 5 secondes appelé');
    var objets = await envoyerRequeteAjax('/api/accueil_asynchrone', "GET", null, null);
    console.log('Réponse de la requête AJAX :', objets);
}

function initialisation() {
    console.log("LOAD")
    setInterval(accueil_au_5_seconde, 5000);
}

window.addEventListener("load", initialisation);

