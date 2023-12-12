"use strict";

let controleur = null;


var la_div = document.getElementById("divDesRecherches");


async function ajout_info_recherche() {
    la_div.innerHTML = "";
    var input = document.getElementById("contenu").value
    input.trim()

    const parametres = {
        "mots-cles": input
    }

    controleur = new AbortController();


    if (input.length > 2) {
        var resultats = await envoyerRequeteAjax('/api/recherche', "GET", parametres, controleur);

        for (var i = 0; i < resultats.length; i++) {
            var nouveau_resultat = document.createElement("input");

            nouveau_resultat.type = "button"
            nouveau_resultat.value = resultats[i].titre
            nouveau_resultat.className = "btn fs-4 d-block px-2 border-3 border-dark rounded";
            nouveau_resultat.id = "propo" + i;
            nouveau_resultat.setAttribute("le_contenu", resultats[i].titre);
            nouveau_resultat.addEventListener("click", rechercher)

            la_div.appendChild(nouveau_resultat)
        }
    }

}


async function rechercher(event){
    var le_contenue = event.currentTarget.getAttribute('le_contenu');
    var input = document.getElementById("contenu")
    input.value = le_contenue
    var le_formulaire = document.getElementById("form_recherche")
    le_formulaire.submit()
}


async function vider_la_div() {
    await new Promise(resolve => setTimeout(resolve, 50))
    la_div.innerHTML = "";
}


async function remplire_la_div() {
    var resultats = await envoyerRequeteAjax('/api/les_recherches', "GET", null, null);
    resultats.reverse();
        for (var i = 0; i < resultats.length; i++) {
            var nouveau_resultat = document.createElement("input");

            nouveau_resultat.type = "button"
            nouveau_resultat.value = resultats[i]
            nouveau_resultat.className = "btn fs-4 d-block px-2 border-3 border-dark rounded";
            nouveau_resultat.id = "propo" + i;
            nouveau_resultat.setAttribute("le_contenu", resultats[i]);
            nouveau_resultat.addEventListener("click", rechercher)

            la_div.appendChild(nouveau_resultat)
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