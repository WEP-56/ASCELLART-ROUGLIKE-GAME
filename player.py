from LOGIC.rouge import Rouge

class Player:
    def __init__(self, name):
        self.name = name
        self.rouge = Rouge()
        self.base_stats = self.rouge.get_player_base_stats()

        # Permanent progression
        self.permanent_health = self.base_stats['health']['initial']
        self.permanent_attack = self.base_stats['attack']['initial']
        self.permanent_defense = self.base_stats['defense']['initial']

        # Initialize player's stats with initial values
        self.health = self.permanent_health
        self.attack = self.permanent_attack
        self.defense = self.permanent_defense

        # In-game progression
        self.soul_crystals = 0
        self.unlocked_items = []
        
        # In-game state
        self.current_health = self.health
        self.current_attack = self.attack
        self.current_defense = self.defense
        self.current_genre = None
        self.current_skills = []
        self.energy = 0
        self.holy_light_value = 0
        self.dark_energy_layers = 0
        self.shadow_energy = 0
        self.summons = []

    def upgrade_permanent_stat(self, stat_name):
        cost = 10 # As defined in GAMEWINDOW.py
        if self.soul_crystals >= cost:
            self.soul_crystals -= cost
            if stat_name == 'health':
                self.permanent_health += 5 # Or whatever the increment is
            elif stat_name == 'attack':
                self.permanent_attack += 2
            elif stat_name == 'defense':
                self.permanent_defense += 1
            return True
        return False

    def upgrade_stat(self, stat_name):
        if stat_name in self.base_stats:
            stat = self.base_stats[stat_name]
            if self.soul_crystals >= stat['upgrade_cost'] and stat['max_upgrades'] > 0:
                self.soul_crystals -= stat['upgrade_cost']
                if stat_name == 'health':
                    self.health += stat['upgrade_amount']
                elif stat_name == 'attack':
                    self.attack += stat['upgrade_amount']
                elif stat_name == 'defense':
                    self.defense += stat['upgrade_amount']
                stat['max_upgrades'] -= 1
                return True
        return False

    def choose_genre(self, genre_name):
        genre = self.rouge.get_genre(genre_name)
        if genre:
            self.current_genre = genre
            # Reset skills when a new genre is chosen
            self.current_skills = []
            return True
        return False

    def add_skill(self, skill_name):
        if self.current_genre:
            for skill in self.current_genre['skills']:
                if skill['name'] == skill_name and skill not in self.current_skills:
                    self.current_skills.append(skill)
                    return True
        return False
        
    def apply_in_game_option(self, option_name):
        for option in self.rouge.get_basic_options():
            if option['name'] == option_name:
                effect = float(option['effect'].strip('%')) / 100
                if '攻击' in option_name:
                    self.current_attack *= (1 + effect)
                elif '生命' in option_name:
                    self.current_health *= (1 + effect)
                    self.health *= (1 + effect)
                elif '防御' in option_name:
                    self.current_defense *= (1 + effect)
                elif '吸血' in option_name:
                    # Lifesteal logic needs to be implemented during combat
                    pass
                return True
        return False

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.current_defense)
        self.current_health -= actual_damage
        return actual_damage

    def deal_damage(self):
        # This is a simplified damage calculation. 
        # It should be expanded with genre and skill effects.
        return self.current_attack

    def reset_for_new_game(self):
        self.health = self.permanent_health
        self.attack = self.permanent_attack
        self.defense = self.permanent_defense
        self.current_health = self.health
        self.current_attack = self.attack
        self.current_defense = self.defense
        self.current_genre = None
        self.current_skills = []
        self.energy = 0
        self.holy_light_value = 0
        self.dark_energy_layers = 0
        self.shadow_energy = 0
        self.summons = []

    def to_dict(self):
        return {
            'name': self.name,
            'permanent_health': self.permanent_health,
            'permanent_attack': self.permanent_attack,
            'permanent_defense': self.permanent_defense,
            'soul_crystals': self.soul_crystals,
            'unlocked_items': self.unlocked_items,
            'base_stats': self.base_stats
        }

    @classmethod
    def from_dict(cls, data):
        player = cls(data['name'])
        player.permanent_health = data.get('permanent_health', player.base_stats['health']['initial'])
        player.permanent_attack = data.get('permanent_attack', player.base_stats['attack']['initial'])
        player.permanent_defense = data.get('permanent_defense', player.base_stats['defense']['initial'])
        player.soul_crystals = data['soul_crystals']
        player.unlocked_items = data['unlocked_items']
        player.base_stats = data['base_stats']
        # Reset stats to permanent values upon loading
        player.reset_for_new_game()
        return player
