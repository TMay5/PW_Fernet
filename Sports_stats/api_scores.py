from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

printer = PrettyPrinter()

def get_links():
    data = get(BASE_URL + ALL_JSON).json()
    links = data['links']
    return links


def get_scoreboard():
    scoreboard = get_links()['currentScoreboard']
    games = get(BASE_URL + scoreboard).json()['games']

    for game in games:
        home_team = game['hTeam']
        away_team = game['vTeam']
        clock = game['clock']
        period = game['period']

        print("-----------------------------------------------")
        print(f"{home_team['triCode']} vs {away_team['triCode']}")
        print(f"{home_team['score']} - {away_team['score']}")
        print(f"{clock} - {period['current']}")

def get_stats():
    stats = get_links()['leagueTeamStatsLeaders']
    teams = get(BASE_URL + stats).json()['league']['standard']['preseason']['teams'] 
    # 'preseason' in 32 has to be altered to 'regularSeason' / 'seasonYear' / 'playoffs' depending on the time of year

    teams = list(filter(lambda x: x['name'] != "Team", teams)) #removes teams with "Team" in their name, as they are not relevant to the data set
    teams.sort(key=lambda x: int(x['ppg']['rank'])) #sorts data by rank and ppg, descending 1-30

    print(f"№|  City  |  Name  |  PPG  |\n"
          "=--------------------------=")
    
    for i, team in enumerate(teams):
        name = team['name']
        nickname = team['nickname']
        ppg = team['ppg']['avg'] #ppg = points per game
        print(f"{i+1}. {name} - {nickname} - {ppg}")

get_stats()
