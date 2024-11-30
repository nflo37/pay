class Game:
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        self.position = 20  # Starting at 20 yard line
        self.down = 1
        self.yards_to_go = 10
        self.score_home = 0
        self.score_away = 0
        self.possession = 'home'  # 'home' or 'away'
        self.play_chart = PlayChart()
        
    def make_move(self, play_type):
        # Basic moves: run or pass
        if play_type == 'run':
            yards = 3  # Simple fixed value for now
        else:  # pass
            yards = 7  # Simple fixed value for now
            
        self.position += yards
        
        # Check if first down
        if yards >= self.yards_to_go:
            self.down = 1
            self.yards_to_go = 10
        else:
            self.down += 1
            self.yards_to_go -= yards
            
        # Check if touchdown
        if self.position >= 100:
            if self.possession == 'home':
                self.score_home += 7
            else:
                self.score_away += 7
            self.reset_possession()
            
        # Check if turnover on downs
        if self.down > 4:
            self.reset_possession()
            
    def reset_possession(self):
        self.position = 20
        self.down = 1
        self.yards_to_go = 10
        self.possession = 'away' if self.possession == 'home' else 'home'
        
    def get_game_state(self):
        return {
            'position': self.position,
            'down': self.down,
            'yards_to_go': self.yards_to_go,
            'score_home': self.score_home,
            'score_away': self.score_away,
            'possession': self.possession,
            'play_chart': self.play_chart.to_dict()  # Convert to dictionary
        }

class Player:
    def __init__(self, name):
        self.name = name
        # Other player attributes

class Board:
    def __init__(self):
        # Initialize board state
        pass

class PlayChart:
    def __init__(self):
        self.running = {
            "Line Plunge": [2, 3, 3, 3, 4, 4, 4, 5, 5, 11, "OFF-2"],
            "Off Tackle": [1, 2, 3, 4, 4, 5, 6, 7, 12, 15, "OFF-3"],
            "End Run": [-2, -1, 2, 3, 4, 5, 8, 12, 20, "OFF-5"],
            "Draw": [-2, 0, 1, 2, 4, 5, 8, 15, 25, "OFF-4"],
            "Screen": [-3, -1, 0, 2, 4, 8, 12, 20, 35, "OFF-6"]
        }
        
        self.passing = {
            "Short Pass": [-2, 0, 0, 4, 6, 8, 10, 12, 15, "INT"],
            "Medium Pass": [-5, -2, 0, 0, 5, 8, 12, 15, 25, "INT"],
            "Long Pass": [-8, -5, -2, 0, 0, 12, 15, 25, 40, "INT"],
            "Screen Pass": [-3, -1, 0, 2, 4, 8, 12, 20, 35, "OFF-3"]
        }
        
        self.special = {
            "Punt": [35, 38, 40, 42, 45, 48, 50, 52, 55],
            "Field Goal": ["Miss", "Miss", "Miss", "Good", "Good", "Good"]
        }

    def get_play_result(self, play_type, play_name):
        """
        Returns a random result from the possible outcomes for the selected play
        """
        import random
        
        if play_type == "run":
            return random.choice(self.running.get(play_name, [0]))
        elif play_type == "pass":
            return random.choice(self.passing.get(play_name, [0]))
        elif play_type == "special":
            return random.choice(self.special.get(play_name, [0]))
        return 0

    def get_available_plays(self, play_type):
        """
        Returns list of available plays for the given play type
        """
        if play_type == "run":
            return list(self.running.keys())
        elif play_type == "pass":
            return list(self.passing.keys())
        elif play_type == "special":
            return list(self.special.keys())
        return []

    def to_dict(self):
        return {
            'running': self.running,
            'passing': self.passing,
            'special': self.special
        }

    @classmethod
    def from_dict(cls, data):
        chart = cls()
        if data:
            chart.running = data.get('running', {})
            chart.passing = data.get('passing', {})
            chart.special = data.get('special', {})
        return chart