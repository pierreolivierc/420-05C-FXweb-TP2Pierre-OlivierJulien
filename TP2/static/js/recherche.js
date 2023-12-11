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

        for (var i = resultats.length; i > 0; i--) {
            var nouveau_resultat = document.createElement("a");

            nouveau_resultat.href = "/objet/troqueur/" + resultats[i].id;
            nouveau_resultat.className = "bg-light p-2 text-decoration-none text-black px-5 border-3 border-dark rounded";
            nouveau_resultat.id = "propo" + i;
            var nom = document.createTextNode(resultats[i].titre);
            nouveau_resultat.appendChild(nom);
            var li = document.createElement("li");
            li.className = "bg-transparent py-2 btn"
            li.appendChild(nouveau_resultat)

            la_div.appendChild(li);
        }
    }

}


async function vider_la_div() {
    la_div.innerHTML = "";
}


async function remplire_la_div() {
    var resultats = await envoyerRequeteAjax('/api/les_recherches', "GET", null, null);

    for (var i = 0; i < resultats.length; i++) {
        var nouveau_resultat = document.createElement("a");

        nouveau_resultat.href = "/objet/rechercher?contenue=" + resultats[i];
        nouveau_resultat.className = "bg-light p-2 text-decoration-none text-black px-5 border-3 border-dark rounded";
        nouveau_resultat.id = "propo" + i;
        var nom = document.createTextNode(resultats[i]);
        nouveau_resultat.appendChild(nom);
        var li = document.createElement("li");
        li.className = "bg-transparent py-2"
        li.appendChild(nouveau_resultat)

        la_div.appendChild(li);
    }
}

function initialisation() {
    document
        .getElementById("contenu")
        .addEventListener("input", ajout_info_recherche);
    document
        .getElementById("contenu")
        .addEventListener("focusout", vider_la_div);
    document
        .getElementById("contenu")
        .addEventListener("focus", remplire_la_div);
}

window.addEventListener("load", initialisation);