import random
import json
import os

class Game:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2
        self.player_team = team1  # Player is always team1 for now
        self.reset_game()
    
    def reset_game(self):
        self.position = 20  # Starting at 20 yard line
        self.down = 1
        self.yards_to_go = 10
        self.team1_score = 0
        self.team2_score = 0
        self.offense = self.team1  # Team1 starts with the ball
        self.defense = self.team2
        # Load both playsheets
        self.team1_playsheet = PlaySheet(self.team1)
        self.team2_playsheet = PlaySheet(self.team2)
    
    @property
    def current_playsheet(self):
        """Returns offensive or defensive plays based on player's team"""
        if self.player_team == self.team1:
            # If player is team1
            return (self.team1_playsheet, True) if self.offense == self.team1 else (self.team1_playsheet, False)
        else:
            # If player is team2
            return (self.team2_playsheet, True) if self.offense == self.team2 else (self.team2_playsheet, False)

    def reset_possession(self):
        """Switch possession between teams"""
        self.position = 20
        self.down = 1
        self.yards_to_go = 10
        self.offense, self.defense = self.defense, self.offense

    def get_game_state(self):
        return {
            'position': self.position,
            'down': self.down,
            'yards_to_go': self.yards_to_go,
            'team1_score': self.team1_score,
            'team2_score': self.team2_score,
            'offense': self.offense,
            'defense': self.defense,
            'team1': self.team1,
            'team2': self.team2,
            'player_team': self.player_team
        }

    def load_state(self, state):
        """Loads game state from a dictionary"""
        self.position = state.get('position', self.position)
        self.down = state.get('down', self.down)
        self.yards_to_go = state.get('yards_to_go', self.yards_to_go)
        self.team1_score = state.get('team1_score', self.team1_score)
        self.team2_score = state.get('team2_score', self.team2_score)
        self.offense = state.get('offense', self.offense)
        self.defense = state.get('defense', self.defense)
        self.team1 = state.get('team1', self.team1)
        self.team2 = state.get('team2', self.team2)
        self.player_team = state.get('player_team', self.player_team)

    def execute_play(self, play_type):
        # Generate random number between 10-39
        roll = random.randint(10, 39)
        
        # Get the outcome based on whether we're on offense or defense
        playsheet, is_offense = self.current_playsheet
        plays = playsheet.offensive_plays if is_offense else playsheet.defensive_plays
        outcome = plays[play_type][str(roll)]
        
        # Process the outcome
        result = self._process_outcome(outcome)
        result['roll'] = roll
        
        return result
    
    def _process_outcome(self, outcome):
        result = {
            'yards': 0,
            'message': '',
            'type': 'normal'
        }
        
        # Handle special outcomes
        if outcome == 'B' or outcome == 'X':
            result['type'] = 'special'
            result['message'] = f"Special play: {outcome}"
            return result
            
        # Handle penalties
        if 'DEF' in outcome:
            yards = int(outcome.split()[1].replace('X', ''))
            self.position += yards
            self.down = 1
            self.yards_to_go = 10
            result['yards'] = yards
            result['type'] = 'defensive_penalty'
            result['message'] = f"Defensive penalty: {yards} yards, automatic first down"
            
        elif 'OFF' in outcome:
            yards = int(outcome.split()[1])
            self.position -= yards
            result['yards'] = -yards
            result['type'] = 'offensive_penalty'
            result['message'] = f"Offensive penalty: {yards} yards back"
            
        else:
            # Normal play
            yards = int(outcome)
            self.position += yards
            result['yards'] = yards
            result['message'] = f"Gained {yards} yards"
            
            # Update downs
            if yards >= self.yards_to_go:
                self.down = 1
                self.yards_to_go = 10
                result['message'] += ", FIRST DOWN!"
            else:
                self.down += 1
                self.yards_to_go -= yards
        
        # Check for touchdown
        if self.position >= 100:
            if self.offense == self.team1:
                self.team1_score += 7
            else:
                self.team2_score += 7
            self.reset_possession()
            result['message'] += " TOUCHDOWN!"
            
        # Check for turnover on downs
        if self.down > 4:
            self.reset_possession()
            result['message'] += " Turnover on downs."
            
        return result

class Player:
    def __init__(self, name):
        self.name = name
        # Other player attributes

class Board:
    def __init__(self):
        # Initialize board state
        pass


class PlaySheet:
    playbooks_dir = os.path.join('data', 'playbooks')
    
    def __init__(self, team_name):
        self.team_name = team_name
        self.offensive_plays = {}
        self.defensive_plays = {}
        self.load_playbook()
    
    def load_playbook(self):
        playbook_path = os.path.join(self.playbooks_dir, f'{self.team_name.lower().replace(" ", "_")}.json')
        with open(playbook_path, 'r') as f:
            data = json.load(f)
            self.offensive_plays = data['offensive_plays']
            self.defensive_plays = data['defensive_plays']

    def get_play_outcomes(self, play_name, is_offense=True):
        """Get all possible outcomes for a specific play."""
        plays = self.offensive_plays if is_offense else self.defensive_plays
        return plays.get(play_name)

    @staticmethod
    def get_available_teams():
        """Return list of teams with available playbooks."""
        teams = []
        
        # List all JSON files in the playbooks directory
        for filename in os.listdir(PlaySheet.playbooks_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(PlaySheet.playbooks_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    teams.append(data['team_name'])
        
        return sorted(teams)