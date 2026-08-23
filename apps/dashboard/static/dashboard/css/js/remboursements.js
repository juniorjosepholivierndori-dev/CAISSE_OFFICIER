const mecano = document.getElementById("mecano");
const nom = document.getElementById("nom");
const prenom = document.getElementById("prenom");
const montantPret = document.getElementById("montant_pret");
const montantVerse = document.getElementById("montant_verse");
const reste = document.getElementById("reste_a_payer");

let pretId = null;

const pretIdInput = document.getElementById("pret_id");


// =====================================================
// RECHERCHE DU MÉCANO
// =====================================================

mecano.addEventListener("input", function () {

    const valeur = this.value.trim();

    // Si le champ est vide
    if (valeur === "") {

        pretId = null;
        pretIdInput.value = "";

        nom.value = "";
        prenom.value = "";
        montantPret.value = "";
        montantVerse.value = "";
        reste.value = "";

        return;
    }


    // Recherche du mécano
    fetch(
        `/api/rechercher-mecano/?mecano=${encodeURIComponent(valeur)}`
    )

        .then(response => response.json())

        .then(data => {

            if (data.success) {

                // Récupération de l'ID du prêt
                pretId = data.pret_id;

                // Mise de l'ID dans le champ caché
                pretIdInput.value = pretId;


                // Informations du mécano
                nom.value = data.nom;

                prenom.value = data.prenom;


                // Montant du prêt
                montantPret.value = data.montant_pret;


                // Calcul du reste
                calculerReste();

            } else {

                pretId = null;
                pretIdInput.value = "";

                nom.value = "";
                prenom.value = "";
                montantPret.value = "";
                reste.value = "";

            }

        })

        .catch(error => {

            console.error(
                "Erreur lors de la recherche :",
                error
            );

        });

});


// =====================================================
// CALCUL DU RESTE À PAYER
// =====================================================

montantVerse.addEventListener(
    "input",
    function () {
        calculerReste();
    }
);


function calculerReste() {

    const pret =
        parseFloat(montantPret.value) || 0;

    const verse =
        parseFloat(montantVerse.value) || 0;


    reste.value = Math.max(
        pret - verse,
        0
    );
}