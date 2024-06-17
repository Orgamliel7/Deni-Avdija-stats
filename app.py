from flask import Flask, render_template
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats

app = Flask(__name__)

# Fetching Deni data
player_dict = players.get_players()
deni_avdija = [player for player in player_dict if player['full_name'] == 'Deni Avdija'][0]
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
        'points_per_game': latest_season['PTS'] / latest_season['GP'],  # Points per game
        'rebounds_per_game': latest_season['REB'] / latest_season['GP'],  # Rebounds per game
        'assists_per_game': latest_season['AST'] / latest_season['GP'],  # Assists per game
        'field_goal_percentage': latest_season['FG_PCT'] * 100,  # Field goal percentage
        'three_point_percentage': latest_season['FG3_PCT'] * 100,  # Three-point percentage
        'free_throw_percentage': latest_season['FT_PCT'] * 100  # Free throw percentage
    }

    return render_template('stats.html', stats=stats_data)

@app.route('/video')
def video():
    return render_template('video.html')


if __name__ == '__main__':
    app.run(debug=True)
