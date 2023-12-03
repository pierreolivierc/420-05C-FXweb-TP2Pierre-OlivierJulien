"use strict";

let controleur = null;

async function ajout_info_recherche() {
    var input = document.getElementById("contenu").value
    input.trim()

    const parametres = {
        "mots-cles": input
    }

    controleur = new AbortController();

    if (input.length > 2) {
        var resultats = envoyerRequeteAjax('/api/recherche', "GET", parametres, controleur);
        await resultats
        resultats = resultats.then()
        console.log(resultats);
        var la_div = document.getElementById("divDesRecherches");
        console.log("etape 1");

        for (var item in resultats){
            console.log(item.id)
        }

        for (var i = 0; i < resultats.length; i++) {
            console.log("Dans boucle")
            var nouveau_resultat = document.createElement("a");

            nouveau_resultat.href = "/objet/troqueur/" + resultats[i].id;
            nouveau_resultat.className = "bg-light p-2 text-decoration-none text-black px-5 border-3 border-dark rounded";
            var nom = document.createTextNode(resultats[i].titre);
            nouveau_resultat.appendChild(nom);
            la_div.appendChild(nouveau_resultat);
            console.log("ajouter");
        }
    }

}


function initialisation() {
    document
        .getElementById("contenu")
        .addEventListener("input", ajout_info_recherche);
}

window.addEventListener("load", initialisation);