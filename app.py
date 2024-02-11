from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

resultats = []
time_data= []

@app.route('/api/recevoir-resultats', methods=['POST'])
def recevoir_resultats():
    session_id = request.form.get('session_id')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    progression_tp = request.form.get('progression_tp')
    difficulte = request.form.get('difficulte')
    progression = request.form.get('progression')
    titre = request.form.get('titre') 
    
    resultats.append({
        'session_id': session_id,
        'nom': nom,  
        'prenom': prenom,
        'progression_tp': progression_tp,
        'difficulte': difficulte,
        'progression': progression,
        'titre': titre
    })

    return 'Données reçues avec succès', 200

@app.route('/api/moyenne-resultats', methods=['GET'])
def moyenne_resultats():
    if not resultats:
        return 'Aucun résultat disponible', 404

    grouped_results = {}
    for res in resultats:
        key = f"{res['prenom']} {res['nom']}"  # Convert the tuple to a string
        if key not in grouped_results:
            grouped_results[key] = []
        grouped_results[key].append({
            'session_id': res['session_id'],
            'progression_tp': res['progression_tp'],
            'difficulte': res['difficulte'],
            'progression': res['progression'],
            #'titre' : res['titre']
        })

    # Return JSON with the grouped results
    return jsonify(grouped_results), 200

@app.route('/api/time_opened', methods=['POST'])
def time_opened():
    time_opened = request.form.get('time_opened')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    cours = request.form.get('cours')
    time_data.append({
        'time_opened': time_opened,
        'nom': nom,
        'prenom': prenom,
        'cours': cours
    })

    return 'Time received successfully', 200

@app.route('/api/time_opened_get', methods=['GET'])
def time_opened_get():
    if not time_data:
        return 'Aucun résultat disponible', 404
    else:
        return jsonify(time_data), 200


if __name__ == '__main__':
    app.run(debug=True)