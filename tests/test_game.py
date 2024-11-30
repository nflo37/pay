import unittest
import os
import json
from game import PlaySheet

class TestPlaySheet(unittest.TestCase):
    def setUp(self):
        # Create a temporary test directory and playbooks
        self.test_playbooks_dir = os.path.join('tests', 'test_playbooks')
        os.makedirs(self.test_playbooks_dir, exist_ok=True)
        
        # Create some test playbook files
        self.test_teams = ["Test Team 1", "Test Team 2", "Test Team 3"]
        
        for team in self.test_teams:
            filename = f"{team.lower().replace(' ', '_')}.json"
            filepath = os.path.join(self.test_playbooks_dir, filename)
            
            test_playbook = {
                "team_name": team,
                "offensive_plays": {},
                "defensive_plays": {}
            }
            
            with open(filepath, 'w') as f:
                json.dump(test_playbook, f)

    def tearDown(self):
        # Clean up test files
        for filename in os.listdir(self.test_playbooks_dir):
            os.remove(os.path.join(self.test_playbooks_dir, filename))
        os.rmdir(self.test_playbooks_dir)

    def test_get_available_teams(self):
        # Temporarily override the playbooks directory
        original_dir = os.path.join('data', 'playbooks')
        PlaySheet.playbooks_dir = self.test_playbooks_dir
        
        # Get available teams
        available_teams = PlaySheet.get_available_teams()
        
        # Reset the playbooks directory
        PlaySheet.playbooks_dir = original_dir
        
        # Verify the results
        self.assertEqual(len(available_teams), len(self.test_teams))
        self.assertEqual(sorted(available_teams), sorted(self.test_teams))

if __name__ == '__main__':
    unittest.main() 