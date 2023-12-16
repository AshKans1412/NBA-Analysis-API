import requests
import pandas as pd
from bs4 import BeautifulSoup

def data_scrapper():
  url = "https://www.basketball-reference.com/leagues/NBA_2024_per_game.html"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  table = soup.find("table", {"id": "per_game_stats"})
  
  
  headers = [ "Player", "Pos", "Age", "Tm", "G", "GS", "MP", "FG", "FGA", "FG%", "3P", "3PA", "3P%",
             "2P", "2PA", "2P%", "eFG%", "FT", "FTA", "FT%", "ORB", "DRB", "TRB", "AST", "STL", "BLK",
             "TOV", "PF", "PTS"]
  
  # Extract the table rows
  rows = []
  for row in table.find_all("tr"):
      data = [cell.get_text() for cell in row.find_all("td")]
      if data:
          rows.append(data)
  df = pd.DataFrame(rows, columns=headers)
  
  return df 
