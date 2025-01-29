import json
import os
from datetime import datetime

class Highscores:
    def __init__(self):
        # Initialize with empty lists for each mode including burst
        self.scores = {
            "quick": [],     # 10 targets
            "normal": [],    # 20 targets
            "burst": [],     # 30 targets
            "extended": []   # 50 targets
        }
        self.filename = "highscores.json"
        self.last_player_name = ""
        self.load_scores()

    def load_scores(self):
        try:
            if os.path.exists(self.filename):
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    loaded_scores = data.get('scores', {})
                    # Update mode names in loaded data including burst
                    self.scores = {
                        "quick": loaded_scores.get("quick", []),
                        "normal": loaded_scores.get("normal", []),
                        "burst": loaded_scores.get("burst", []),
                        "extended": loaded_scores.get("extended", [])
                    }
                    self.last_player_name = data.get('last_player', "")
        except:
            # Reset scores with all modes including burst
            self.scores = {
                "quick": [],
                "normal": [],
                "burst": [],
                "extended": []
            }
            self.last_player_name = ""

    def save_scores(self):
        with open(self.filename, 'w') as f:
            json.dump({
                'scores': self.scores,
                'last_player': self.last_player_name
            }, f)

    def add_score(self, name, reaction_time, mode):
        self.last_player_name = name
        self.scores[mode].append({
            'name': name, 
            'time': reaction_time,
            'date': datetime.now().strftime('%m/%d/%y')
        })
        self.scores[mode].sort(key=lambda x: x['time'])
        self.scores[mode] = self.scores[mode][:10]  # Keep only top 10
        self.save_scores()

    def get_top_scores(self, mode, limit=10):
        return self.scores.get(mode, [])[:limit]

    def clear_scores(self, mode=None):
        if mode:
            self.scores[mode] = []
        else:
            self.scores = {"quick": [], "normal": [], "burst": [], "extended": []}
        self.save_scores()
