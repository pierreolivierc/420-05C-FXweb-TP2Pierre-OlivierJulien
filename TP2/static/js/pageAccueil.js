"use strict";

async function accueil_au_5_seconde(){
    var objets = await envoyerRequeteAjax('/api/accueil_asynchrone', "GET", null, null);
    var div_objet = document.getElementById('liste_objet_accueil');

    // TODO comparer le dictionnaire a un cookie de session contenant le 5 objet
    if(objets){
       while (div_objet.firstChild) {
        div_objet.removeChild(div_objet.firstChild);
        }

        for (let i=0; i<5; i++) {
            var divElement = document.createElement('div');
            divElement.classList.add('card', 'col-md-12', 'col-lg-6', 'd-flex', 'justify-content-center', 'm-4', 'p-3', 'border-dark');
            divElement.style.width = '18rem';
            div_objet.appendChild(divElement);

            var imageElement = document.createElement('img');
            imageElement.height = 300;
            imageElement.width = 300;
            imageElement.classList.add('card-img-top');
            imageElement.src = objets[i]['photo'];
            divElement.append(imageElement);

            var divCard = document.createElement('div');
            divCard.classList.add('card-body');
            divElement.append(divCard);

            var titreCard = document.createElement('h5');
            titreCard.textContent = objets[i]['titre'];
            titreCard.classList.add('card-title');

            var texteCard = document.createElement('p');
            texteCard.textContent = objets[i]['description'];
            texteCard.classList.add('card-text');

            divCard.append(titreCard, texteCard);

            var divBouton = document.createElement('div');
            divCard.append(divBouton);

            var boutonVoir = document.createElement('a');
            boutonVoir.href = '/objet/details/' + objets[i]['id'];
            boutonVoir.classList.add('btn', 'btn-primary', 'm-2');
            boutonVoir.textContent = 'Voir l\'objet';
            divBouton.appendChild(boutonVoir);
            if (objets) {
                var boutonModifier = document.createElement('a');
                boutonModifier.href = '/objet/modifier/' + objets[i]['id'];
                boutonModifier.classList.add('btn', 'btn-primary', 'm-2');
                boutonModifier.textContent = 'Modifier';
                divBouton.appendChild(boutonModifier);

                var boutonSupprimer = document.createElement('a');
                boutonSupprimer.href = '/objet/supprimer_objet/' + objets[i]['id'];
                boutonSupprimer.classList.add('btn', 'btn-primary', 'm-2');
                boutonSupprimer.textContent = 'Supprimer';
                divBouton.appendChild(boutonSupprimer);
            }

            // TODO vérifier si l'utilisateur n'est pas propriétaire
            if (objets) {
                var boutonTroquer = document.createElement('a');
                boutonTroquer.href = '/objet/troqueur/' + objets[i]['id'];
                boutonTroquer.classList.add('btn', 'btn-primary', 'm-2');
                boutonTroquer.textContent = 'Troquer';
                divBouton.appendChild(boutonTroquer);
            }

        }
    }

}

function initialisation() {
    setInterval(accueil_au_5_seconde, 5000);
}

window.addEventListener("load", initialisation);

