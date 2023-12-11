"use strict";

var la_div = document.getElementById("la_div");
var mot_cle = document.getElementById("mot_cle").innerHTML;
var index

async function charger(i) {
    if ((index - 4 > -1) && (i === 8)){
        index = index - 4;
    }
    else if (i === 4){
        index += i;
    }
    var courrielUtilisateur = await envoyerRequeteAjax('/api/information_utilisateur', "GET", null, null);
    var admin = await envoyerRequeteAjax('/api/information_administateur', "GET", null, null);
    la_div.innerHTML = ""

    const parametres = {
        "mot-cle": "%" + mot_cle + "%",
        "index": index
    }
    controleur = new AbortController();
    var resultats = await envoyerRequeteAjax('/api/les_quatres_suivants', "GET", parametres, controleur);
    for (var i = 0; i < resultats.length; i++){
        if (resultats[i].photo == null){
            resultats[i].photo = "Image_de_base"
        }

        var grosse_div = document.createElement("div");
        grosse_div.className = "card col-md-12 col-lg-6 d-flex justify-content-center m-4 p-3 border-dark";
        grosse_div.style.width = '18rem';

        var image = document.createElement("img")
        image.width = "300";
        image.height = "300";
        image.className = "card-img-top";
        image.src = resultats[i].photo;
        image.alt = "L'image d'un objet";
        grosse_div.appendChild(image);

        var petite_div = document.createElement("div");
        petite_div.className = "card-body"

        var titre = document.createElement("h5");
        titre.className = "card-title";
        var le_titre = document.createTextNode(resultats[i].titre);
        titre.appendChild(le_titre);
        petite_div.appendChild(titre);

        var description = document.createElement("p");
        description.className = "card-text";
        var la_description = document.createTextNode(i.description);
        description.appendChild(la_description);
        petite_div.appendChild(description);

        var plus_petite_div = document.createElement("div")

        var btn_details = document.createElement("a")
        btn_details.href = "/objet/details/" + resultats[i].id
        btn_details.className = "btn btn-primary m-2"
        var texte_btn1 = document.createTextNode("Voir l'objet")
        btn_details.appendChild(texte_btn1)
        plus_petite_div.appendChild(btn_details)

        if ((courrielUtilisateur === resultats[i].proprietaire) || (admin === "1")) {
            var btn_modifier = document.createElement("a")
            btn_modifier.href = "/objet/modifier/" + resultats[i].id
            btn_modifier.className = "btn btn-primary m-2"
            var texte_btn2 = document.createTextNode("Modifier")
            btn_modifier.appendChild(texte_btn2)
            plus_petite_div.appendChild(btn_modifier)

            var btn_supprimer = document.createElement("a")
            btn_modifier.href = "/objet/supprimer_objet/" + resultats[i].id
            btn_modifier.className = "btn btn-primary m-2"
            var texte_btn3 = document.createTextNode("Supprimer")
            btn_supprimer.appendChild(texte_btn3)
            plus_petite_div.appendChild(btn_supprimer)
        }
        if ((courrielUtilisateur !== resultats[i].proprietaire)){
            var btn_troquer = document.createElement("a")
            btn_modifier.href = "/objet/troqueur/" + resultats[i].id
            btn_modifier.className = "btn btn-primary m-2"
            var texte_btn4 = document.createTextNode("Troquer")
            btn_troquer.appendChild(texte_btn4)
            plus_petite_div.appendChild(btn_troquer)
        }

        petite_div.appendChild(plus_petite_div)
        grosse_div.appendChild(petite_div)
        la_div.appendChild(grosse_div)

    }
}


async function precedent(){
    charger(8)
}

async function suivant(){
    charger(4)
}


function initialisation() {
    index = 0
    document
        .getElementById("precedent")
        .addEventListener("click", precedent);
    document
        .getElementById("suivant")
        .addEventListener("click", suivant);
    charger(0)
}

window.addEventListener("load", initialisation);