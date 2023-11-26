from flask import Flask, jsonify, request
import os
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from Assests.ML_Accesspoint import predict_2
from Assests.Data_Scraping import data_scrapper
import pickle 

scaler_file = "Assests/Models/scaler.sav"
svm_file = "Assests/Models/model.sav"
prime_data = "Assests/Datasets/NBA_2024_per_game.csv"
data_predict = "Assests/Datasets/data.csv"

model = pickle.load(open(svm_file,"rb"))
scaler = pickle.load(open(scaler_file,"rb"))

app = Flask(__name__)

nba_data = pd.read_csv(prime_data)
data = pd.read_csv(data_predict)

def scheduled_task():
    try:
        nba_data = data_scrapper()
    except:
        pass
        

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", days=1)
scheduler.start()

#nba_data = pd.read_csv('./NBA_2024_per_game.csv')

@app.route('/')
def home():
    return "Welcome to the NBA 2024 Stats API!"



@app.route('/players', methods=['GET'])
def get_players():
    players = nba_data['Player'].unique().tolist()
    return jsonify(players)


@app.route('/players/<string:name>', methods=['GET'])
def get_player_details(name):
    player_data = nba_data[nba_data['Player'] == name].to_dict(orient='records')
    if player_data:
        return jsonify(player_data)
    else:
        return jsonify({'message': 'Player not found'}), 404


@app.route('/dataset', methods=['GET'])
def get_dataset():
    # Convert the DataFrame to JSON
    data_json = nba_data.to_json(orient='records')
    
    # Return the JSON response
    return jsonify(data_json)


@app.route('/predict', methods=['GET'])
def predict_winner():
    team1 = request.args.get('team1')
    team2 = request.args.get('team2')

    # Your prediction logic here
    winner = predict_2(team1, team2, model, scaler, data)
    
    return jsonify({"Predicted Winner": winner})
    #return jsonify({team1: team2})



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
