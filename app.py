from flask import Flask, render_template, request
import requests

app = Flask(__name__)


def home():
    return render_template('home.html')


def stats():
    stats_data = {
        'season': '2023-2024',
        'games_played': '72',
        'points_per_game': 11.2,
        'rebounds_per_game': 4.5,
        'assists_per_game': 3.1
    }
    return render_template('stats.html', stats=stats_data)

if __name__ == '__main__':
    app.run(debug=True)