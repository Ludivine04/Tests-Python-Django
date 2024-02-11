from flask import Flask, request, jsonify

app = Flask(__name__)  # Création d'une instance de l'application Flask

resultats = []  # Initialisation d'une liste pour stocker les résultats

@app.route('/api/recevoir-resultats', methods=['POST'])
def recevoir_resultats():
    """
    Fonction pour recevoir les résultats envoyés via une requête POST.
    Les données JSON sont extraites de la requête et ajoutées à la liste 'resultats'.
    """
    # Extraction des données JSON de la requête
    donnees = request.json
    # Ajout des données à la liste 'resultats'
    resultats.append(donnees)
    # Réponse HTTP indiquant que les données ont été reçues avec succès
    return 'Données reçues avec succès', 200

@app.route('/api/moyenne-resultats', methods=['GET'])
def moyenne_resultats():
    """
    Fonction pour calculer la moyenne des scores des 5 derniers résultats
    et renvoyer la moyenne sous forme de réponse JSON.
    """
    if not resultats:
        # Si aucun résultat n'est disponible, renvoie une réponse 404
        return 'Aucun résultat disponible', 404

    # Récupération des 5 derniers résultats
    dernieres_resultats = resultats[-5:]
    # Calcul de la moyenne des scores
    moyenne = sum(res['score'] for res in dernieres_resultats) / len(dernieres_resultats)
    # Renvoie une réponse JSON avec la moyenne calculée
    return jsonify({'moyenne': moyenne}), 200

if __name__ == '__main__':
    app.run(debug=True)


