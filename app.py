from flask import Flask, render_template, request, redirect, url_for, session
from game import Game, PlayChart

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def home():
    if 'game_state' not in session:
        game = Game()
        session['game_state'] = game.get_game_state()
    else:
        game = Game()
        state = session['game_state']
        game.position = state['position']
        game.down = state['down']
        game.yards_to_go = state['yards_to_go']
        game.score_home = state['score_home']
        game.score_away = state['score_away']
        game.possession = state['possession']
        game.play_chart = PlayChart.from_dict(state['play_chart'])
    
    return render_template('game.html', game=game)

@app.route('/move', methods=['POST'])
def move():
    if 'game_state' not in session:
        game = Game()
    else:
        game = Game()  # Create new game instance
        # Restore the game state from session
        state = session['game_state']
        game.position = state['position']
        game.down = state['down']
        game.yards_to_go = state['yards_to_go']
        game.score_home = state['score_home']
        game.score_away = state['score_away']
        game.possession = state['possession']
    
    play_type = request.form.get('play_type')
    game.make_move(play_type)
    # Store the new state
    session['game_state'] = game.get_game_state()
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    session['game_state'] = Game().get_game_state()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)