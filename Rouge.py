import json

class Rouge:
    def __init__(self, rouge_file='c:\\Users\\chinese\\PycharmProjects\\ASCELL-ROUGE\\LOGIC\\rouge.json'):
        with open(rouge_file, 'r', encoding='utf-8') as f:
            self.rouge_data = json.load(f)

    def get_player_base_stats(self):
        return self.rouge_data.get('player_base_stats', {})

    def get_genres(self):
        return self.rouge_data.get('genres', [])

    def get_genre(self, genre_name):
        for genre in self.get_genres():
            if genre['name'] == genre_name:
                return genre
        return None

    def get_basic_options(self):
        return self.rouge_data.get('basic_options', [])
