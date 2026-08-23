const formulaire = document.querySelector("form");

formulaire.addEventListener("submit", function (event) {

    const mecano = document.getElementById("mecano").value.trim();

    const nom = document.getElementById("nom").value.trim();

    const prenom = document.getElementById("prenom").value.trim();

    const pays = document.getElementById("pays").value.trim();

    const ville = document.getElementById("ville").value.trim();

    const grade = document.getElementById("grade").value.trim();

    const unite = document.getElementById("unite").value.trim();

    const statut = document.getElementById("statut").value;

    const dateNaissance = document.getElementById("date_naissance").value;

    const telephone = document.getElementById("telephone").value.trim();

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value;

    const confirmPassword = document.getElementById("confirm_password").value;

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;


    if (
        mecano === "" ||
        nom === "" ||
        prenom === "" ||
        pays === "" ||
        ville === "" ||
        grade === "" ||
        unite === "" ||
        statut === "" ||
        dateNaissance === "" ||
        telephone === "" ||
        email === "" ||
        password === "" ||
        confirmPassword === ""
    ) {

        event.preventDefault();

        alert("Veuillez remplir tous les champs.");

        return;
    }


    if (password !== confirmPassword) {

        event.preventDefault();

        alert("Les mots de passe ne correspondent pas.");

        return;
    }


    if (password.length < 8) {

        event.preventDefault();

        alert("Le mot de passe doit contenir au moins 8 caractères.");

        return;
    }


    if (!emailRegex.test(email)) {

        event.preventDefault();

        alert("Veuillez entrer une adresse email valide.");

        return;
    }

});