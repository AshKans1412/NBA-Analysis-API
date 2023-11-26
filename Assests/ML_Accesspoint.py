import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.svm import SVC
import pickle


scaler_file = "./Models/scaler.sav"
svm_file = "./Models/model.sav"


model = pickle.load(open(svm_file,"rb"))
scaler = pickle.load(open(scaler_file,"rb"))


def predict_2(team1, team2, model, label_encoder, scaler, data):    
    mapping = {'ATL': 0, 'BOS': 1, 'BRK': 2, 'CHI': 3, 'CHO': 4, 'CLE': 5, 'DAL': 6, 'DEN': 7, 'DET': 8, 'GSW': 9, 'HOU': 10, 'IND': 11, 'LAC': 12, 'LAL': 13, 'MEM': 14, 'MIA': 15, 'MIL': 16, 'MIN': 17, 'NOP': 18, 'NYK': 19, 'OKC': 20, 'ORL': 21, 'PHI': 22, 'PHO': 23, 'POR': 24, 'SAC': 25, 'SAS': 26, 'TOR': 27, 'UTA': 28, 'WAS': 29}

    team1_encoded = mapping[team1]
    team2_encoded = mapping[team2]
    
    recent_season_data = data[data['season'] == 2022]

    select_cols = ['team_encoded', 'team_opp_encoded', 'season', 'fg%', '3p%', 'ft%', 
                              'orb', 'drb', 'orb%', 'drb%', 'ft%_max', 'fg%_max', '3p%_max', 
                              'fg%_opp', '3p%_opp', 'ft%_opp', 'orb_opp', 'trb_opp', 'orb%_opp', 
                              'drb%_opp', 'ft%_max_opp', 'fg%_max_opp', '3p%_max_opp']
    home = ["season",'team_encoded','fg%','3p%','ft%','orb','drb','orb%','drb%','ft%_max','fg%_max','3p%_max']
    opp = ['team_opp_encoded','fg%_opp','3p%_opp','ft%_opp','orb_opp','trb_opp','orb%_opp','drb%_opp','ft%_max_opp','fg%_max_opp','3p%_max_opp']

    x = recent_season_data[recent_season_data['team_encoded'] == team1_encoded]
    y = recent_season_data[recent_season_data['team_opp_encoded'] == team2_encoded]

    x_mean = x.mean().to_dict()
    y_mean = y.mean().to_dict()
    temp = (pd.concat([pd.DataFrame([x_mean])[home], pd.DataFrame([y_mean])[opp]],axis = 1))
    temp = temp[select_cols]
    feature_vector_scaled = scaler.transform(temp)

    # Predict outcome
    prediction = model.predict(feature_vector_scaled)[0]
    winner = team1 if prediction else team2

    return winner

     
    
                      
