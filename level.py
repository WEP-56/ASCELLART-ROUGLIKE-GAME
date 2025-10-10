import json

class Level:
    def __init__(self, level_file='c:\\Users\\chinese\\PycharmProjects\\ASCELL-ROUGE\\LOGIC\\level.json'):
        with open(level_file, 'r', encoding='utf-8') as f:
            self.levels_data = json.load(f)

    def get_difficulty_levels(self, difficulty):
        return self.levels_data['difficulties'].get(difficulty, {}).get('levels', [])

    def get_level(self, difficulty, level_id):
        levels = self.get_difficulty_levels(difficulty)
        for level in levels:
            if level['id'] == level_id:
                return level
        return None
