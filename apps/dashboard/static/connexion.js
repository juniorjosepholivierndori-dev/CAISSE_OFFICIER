const formulaire = document.querySelector("form");

formulaire.addEventListener("submit", function(event) {

    const email = document.getElementById("email").value.trim();

    const password = document.getElementById("password").value;

    if (email === "") {

        event.preventDefault();

        alert("Veuillez entrer votre adresse email.");

        return;
    }

    if (password === "") {

        event.preventDefault();

        alert("Veuillez entrer votre mot de passe.");

        return;
    }

    if (password.length < 8) {

        event.preventDefault();

        alert("Le mot de passe doit contenir au moins 8 caractères.");

        return;
    }

});
