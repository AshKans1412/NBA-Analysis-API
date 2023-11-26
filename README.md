
# NBA Stats API

## Introduction
This repository, [NBA-Analysis-API](https://github.com/AshKans1412/NBA-Analysis-API.git), hosts the Flask application for the NBA 2024 Stats API. This web service provides up-to-date NBA player statistics for the year 2024, scraping data daily from a basketball reference website. The API is hosted on Heroku for easy and reliable access.

## Features
- Automated daily data scraping for NBA 2024 statistics.
- Accessible API endpoints for retrieving player statistics.
- Hosted on Heroku, ensuring high availability and ease of access.

## Accessing the API

The API is hosted on Heroku and can be accessed at the following base URL: `https://ash-nba-api-ea2ef5de0ea1.herokuapp.com/`

### API Endpoints

- `/` - Welcome message and API information.
- `/players` - Retrieves a list of all NBA players in the dataset.
- `/players/<string:name>` - Provides detailed statistics for a specified player.
- `/dataset` - Returns the entire dataset in JSON format.
- `/predict` - Returns which teams wins.

### Example Request

To fetch details of a specific player:

```
GET https://ash-nba-api-ea2ef5de0ea1.herokuapp.com/players/LeBron James
```

### Example Request for Prediction

To fetch prediction betweem `MIA` & `GSW`: <i>(Considering MIA as Home Team)</i>

```
GET https://ash-nba-api-ea2ef5de0ea1.herokuapp.com/predict?team1=MIA&team2=GSW
```

## Local Setup

To run the API locally:

1. Clone the repository:
   ```
   git clone https://github.com/AshKans1412/NBA-Analysis-API.git
   cd NBA-Analysis-API
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Flask app:
   ```
   python app.py
   ```

## Technologies

- Flask
- Pandas
- APScheduler
- Requests
- BeautifulSoup

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.


## License

This project is licensed under the MIT License - see the LICENSE file for details.
