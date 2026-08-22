document.addEventListener("DOMContentLoaded", async () => {
    try {
        const response = await fetch("/api/profil/");

        if (!response.ok) {
            throw new Error("Impossible de charger le profil");
        }

        const profil = await response.json();

        const champs = {
            "Mécano": profil.mecano,
            "Nom": profil.nom,
            "Prénom": profil.prenom,
            "Grade": profil.grade,
            "Unité": profil.unite,
            "Pays": profil.pays,
            "Ville": profil.ville,
            "Statut": profil.statut,
            "Téléphone": profil.telephone,
            "Email": profil.email
        };

        document.querySelectorAll(".info-row").forEach((ligne) => {
            const label = ligne.querySelector(".label")?.textContent.trim();
            const valeur = ligne.querySelector(".value");

            if (valeur && champs[label] !== undefined) {
                valeur.textContent = champs[label] || "";
            }
        });

    } catch (error) {
        console.error("Erreur :", error);
    }
});


document.addEventListener("DOMContentLoaded", () => {

    const boutons = document.querySelectorAll(".menu-item");

    boutons.forEach((bouton) => {

        bouton.addEventListener("click", () => {

            boutons.forEach((item) => {
                item.classList.remove("active");
            });

            bouton.classList.add("active");
        });

    });

});