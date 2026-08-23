document.addEventListener("DOMContentLoaded", function () {

    const nombreTotal = document.getElementById("nombre-total");
    const montantTotal = document.getElementById("montant-total");
    const cotisationsBody = document.getElementById("cotisations-body");


    if (!cotisationsBody) {
        return;
    }

    const lignes = cotisationsBody.querySelectorAll("tr");



    if (lignes.length > 0) {

        let nombre = 0;
        let total = 0;

        lignes.forEach(function (ligne) {

            const cellules = ligne.querySelectorAll("td");


            if (cellules.length === 4) {

                nombre++;

                const montantTexte = cellules[3].textContent
                    .replace("FCFA", "")
                    .replace(/\s/g, "")
                    .replace(",", ".");

                const montant = parseFloat(montantTexte);

                if (!isNaN(montant)) {
                    total += montant;
                }
            }
        });

        nombreTotal.textContent = nombre;

        montantTotal.textContent =
            total.toLocaleString("fr-FR") + " FCFA";
    }

});