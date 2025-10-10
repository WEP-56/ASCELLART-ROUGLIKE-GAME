import json
import os
from CODE.player import Player

class SaveManager:
    def __init__(self, save_dir='saves'):
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def save_player(self, player):
        save_data = player.to_dict()
        save_file = os.path.join(self.save_dir, f'{player.name}.json')
        with open(save_file, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)

    def load_player(self, player_name):
        save_file = os.path.join(self.save_dir, f'{player_name}.json')
        if os.path.exists(save_file):
            with open(save_file, 'r', encoding='utf-8') as f:
                player_data = json.load(f)
                return Player.from_dict(player_data)
        return None

    def player_exists(self, player_name):
        save_file = os.path.join(self.save_dir, f'{player_name}.json')
        return os.path.exists(save_file)
