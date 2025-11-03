import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, history_file='policy_history.json'):
        self.history_file = history_file
        self.history = self._load_history()
    
    def _load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []
    
    def save_policy(self, requirement, policy, rationale):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'requirement': requirement,
            'policy': policy,
            'rationale': rationale
        }
        self.history.append(entry)
        self._save_history()
        return len(self.history) - 1
    
    def _save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def get_history(self):
        return self.history
    
    def get_policy(self, index):
        if 0 <= index < len(self.history):
            return self.history[index]
        return None