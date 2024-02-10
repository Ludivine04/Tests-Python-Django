from flask import Flask, request, jsonify

app = Flask(__name__)  # Création d'une instance de l'application Flask

resultats = []  # Initialisation d'une liste pour stocker les résultats

@app.route('/api/recevoir-resultats', methods=['POST'])  # Définition de la route pour recevoir les résultats
def recevoir_resultats():
    """
    Cette fonction gère les requêtes POST pour recevoir de nouveaux résultats.
    Les données JSON sont extraites de la requête et ajoutées à la liste 'resultats'.
    """
    donnees = request.json  # Extraction des données JSON de la requête
    resultats.append(donnees)  # Ajout des données à la liste 'resultats'
    return 'Données reçues avec succès', 200  # Réponse HTTP indiquant que les données ont été reçues

@app.route('/api/moyenne-resultats', methods=['GET'])  # Définition de la route pour calculer la moyenne des résultats
def moyenne_resultats():
    """
    Cette fonction gère les requêtes GET pour calculer la moyenne des 5 derniers résultats.
    Si aucun résultat n'est disponible, elle renvoie un message indiquant qu'aucun résultat n'est disponible.
    Sinon, elle calcule la moyenne des scores et renvoie une réponse JSON contenant la moyenne.
    """
    if not resultats:  # Vérification si des résultats sont disponibles
        return 'Aucun résultat disponible', 404  # Si aucun résultat n'est disponible, renvoie une réponse 404

    dernieres_resultats = resultats[-5:]  # Récupération des 5 derniers résultats
    moyenne = sum(res['score'] for res in dernieres_resultats) / len(dernieres_resultats)  # Calcul de la moyenne
    return jsonify({'moyenne': moyenne}), 200  # Renvoie une réponse JSON avec la moyenne calculée

if __name__ == '__main__':
    app.run(debug=True)  # Démarrage de l'application Flask en mode debug si le script est exécuté directement


