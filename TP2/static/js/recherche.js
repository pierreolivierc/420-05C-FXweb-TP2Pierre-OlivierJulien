"use strict";

let controleur = null;



var la_div = document.getElementById("divDesRecherches");



async function ajout_info_recherche() {
    var input = document.getElementById("contenu").value
    input.trim()

    const parametres = {
        "mots-cles": input
    }

    controleur = new AbortController();

    vider_la_div()

    if (input.length > 2) {
        var resultats = await envoyerRequeteAjax('/api/recherche', "GET", parametres, controleur);

        for (var i = 0; i < resultats.length; i++) {
            var nouveau_resultat = document.createElement("a");

            nouveau_resultat.href = "/objet/troqueur/" + resultats[i].id;
            nouveau_resultat.className = "bg-light p-2 text-decoration-none text-black px-5 border-3 border-dark rounded";
            nouveau_resultat.id = "propo" + i;
            var nom = document.createTextNode(resultats[i].titre);
            nouveau_resultat.appendChild(nom);
            la_div.appendChild(nouveau_resultat);
        }
    }

}


async function vider_la_div(){
        la_div.innerHTML = "";
}



function initialisation() {
    document
        .getElementById("contenu")
        .addEventListener("input", ajout_info_recherche);
    document
        .getElementById("contenu")
        .addEventListener("focusout", vider_la_div);
}

window.addEventListener("load", initialisation);