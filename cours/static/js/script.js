// Récupérer l'élément HTML où afficher la moyenne des résultats
var moyenneResultatsElement = document.getElementById('moyenne-resultats');

// Effectuer une requête AJAX pour récupérer la moyenne des résultats depuis l'API Flask
fetch('/api/moyenne-resultats')
    .then(response => {
        // Vérifier si la réponse de la requête est OK
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération de la moyenne des résultats depuis l\'API');
        }
        // Renvoyer les données de réponse au format JSON
        return response.json();
    })
    .then(data => {
        // Mettre à jour l'interface utilisateur avec la moyenne des résultats
        moyenneResultatsElement.textContent = 'Moyenne des résultats : ' + data.moyenne;
    })
    .catch(error => {
        // Gérer les erreurs survenues lors de la requête
        console.error('Erreur :', error);
    });

