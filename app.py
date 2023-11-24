from flask import Flask, jsonify
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from Assests.Data_Scraping import data_scrapper

app = Flask(__name__)


def scheduled_task():
    try:
        nba_data = data_scrapper()
    except:
        nba_data = pd.read_csv('./NBA_2024_per_game.csv')
        

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduled_task, trigger="interval", days=1)
scheduler.start()


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



if __name__ == '__main__':
    app.run(debug=True)
