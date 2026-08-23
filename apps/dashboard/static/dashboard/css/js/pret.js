document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("pret-form");
    const boutonAnnuler = document.getElementById("btn-annuler");

    boutonAnnuler.addEventListener("click", function () {
        form.reset();
    });

    form.addEventListener("submit", async function (event) {

        event.preventDefault();

        const token = localStorage.getItem("access_token");

        const donnees = {
            mecano: document.getElementById("matricule").value,
            montant: document.getElementById("montant").value,
            date_pret: document.getElementById("date_pret").value,
            motif: document.getElementById("motif").value,
            duree_remboursement: document.getElementById("duree").value
        };

        const response = await fetch("/api/operations/prets/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(donnees)
        });

        const data = await response.json();

        if (response.ok) {
            alert("Prêt enregistré avec succès !");
            form.reset();
        } else {
            alert(data.detail || "Erreur lors de l'enregistrement.");
        }

    });

});