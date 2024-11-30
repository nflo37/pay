from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from game import Game, PlaySheet

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if 'game_state' not in session:
        return redirect(url_for('select_teams'))
    
    # Get the teams from the session state
    state = session['game_state']
    team1 = state.get('team1')
    team2 = state.get('team2')
    
    # Create game instance with actual team names
    game = Game(team1, team2)
    game.load_state(state)
    
    return render_template('game.html', game=game)

@app.route('/select_teams')
def select_teams():
    available_teams = PlaySheet.get_available_teams()
    return render_template('team_select.html', available_teams=available_teams)

@app.route('/start_game', methods=['POST'])
def start_game():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    player_team = team1  # Player is always team1 for now
    session['player_team'] = player_team
    game = Game(team1, team2)
    session['game_state'] = game.get_game_state()
    return redirect(url_for('home'))

@app.route('/move', methods=['POST'])
def move():
    if 'game_state' not in session:
        return redirect(url_for('select_teams'))
    
    state = session['game_state']
    game = Game(state['team1'], state['team2'])  # Initialize with actual team names
    game.load_state(state)
    
    play_type = request.form.get('play_type')
    result = game.execute_play(play_type)
    session['game_state'] = game.get_game_state()
    return redirect(url_for('home'))

@app.route('/run_play', methods=['POST'])
def run_play():
    if 'game_state' not in session:
        return jsonify({'error': 'No game in progress'}), 400
    
    state = session['game_state']
    game = Game(state['team1'], state['team2'])  # Initialize with actual team names
    game.load_state(state)
    
    data = request.get_json()
    play = data.get('play')
    
    result = game.execute_play(play)
    session['game_state'] = game.get_game_state()
    
    return jsonify({
        'status': 'success',
        'result': result,
        'message': f'Play {play} executed for {game.offense}'
    })

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('select_teams'))

if __name__ == '__main__':
    app.run(debug=True)