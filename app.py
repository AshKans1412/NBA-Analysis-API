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
images= "Assests/Datasets/images_data.csv"

model = pickle.load(open(svm_file,"rb"))
scaler = pickle.load(open(scaler_file,"rb"))


app = Flask(__name__)
bro = "Welcome to the NBA 2024 Stats API!"

nba_data = pd.read_csv(prime_data)
data = pd.read_csv(data_predict)
images_data = pd.read_csv(images)

def scheduled_task():
    try:
        nba_data = data_scrapper()
    except:
        bro = "ceqecercqefrv"
        
# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", seconds=5)
scheduler.start()

#nba_data = pd.read_csv('./NBA_2024_per_game.csv')

@app.route('/')
def home():
    #return "Welcome to the NBA 2024 Stats API!"
    return bro



@app.route('/players', methods=['GET'])
def get_players():
    players = nba_data['Player'].unique().tolist()
    return jsonify(players)


@app.route('/players/<string:name>', methods=['GET'])
def get_player_details(name):
    #player_data = nba_data[nba_data['Player'] == name].to_dict(orient='records')

    '''
    if player_data:
        return jsonify(player_data)
    else:
        return jsonify({'message': 'Player not found'}), 404
    '''
    player_nba_data = nba_data[nba_data['Player'] == name].to_dict(orient='records')
    player_images_data = images_data[images_data['API_Names'] == name].to_dict(orient='records')

    if player_nba_data and player_images_data:
        combined_data = {**player_nba_data[0], **player_images_data[0]}  # Combine the data from both datasets
        return jsonify(combined_data)
    elif player_nba_data:
        return jsonify(player_nba_data)
    elif player_images_data:
        return jsonify(player_images_data)
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

@app.route('/get_images/<string:name>', methods=['GET'])
def get_player_images(name):
    try:
        player_data = images_data[images_data['API_Names'] == name].playerid.values[0]
    except:
        player_data = False
    xxx = "https://raw.githubusercontent.com/AshKans1412/NBA-Analysis-API/main/Assests/img/" + str(player_data) + ".png"
    if player_data:
        return jsonify({"image": xxx })
    else:
        return jsonify({'message': "https://raw.githubusercontent.com/AshKans1412/NBA-Analysis-API/main/Assests/img/default.png"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
