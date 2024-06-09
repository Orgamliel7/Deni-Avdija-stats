from flask import Flask, render_template, request
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

app = Flask(__name__)

# Fetching Deni data
player_dict = players.get_players()
deni_avdija = [player for player in player_dict in players['full_name'] == 'Deni Avdija'][0]
deni_avdija_id = deni_avdija['id']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/stats')
def stats():
    # Fetch career stats
    career = playercareerstats.PlayerCareerStats(player_id=deni_avdija_id)
    career_stats = career.get_data_frames()[0]
    
    # latest season stats
    latest_season = career_stats.iloc[-1]

    stats_data = {
        'season': latest_season['SEASON_ID'],
        'games_played': latest_season['GP'],
        'points_per_game': latest_season['PTS'],
        'rebounds_per_game': latest_season['REB'],
        'assists_per_game': latest_season['AST'],
        'field_goal_percentage': latest_season['FG_PCT'] * 100,
        'three_point_percentage': latest_season['FG3_PCT'] * 100,
        'free_throw_percentage': latest_season['FT_PCT'] * 100
    }
    return render_template('stats.html', stats=stats_data)

if __name__ == '__main__':
    app.run(debug=True)