import sys
import os

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import random
from PyQt5.QtWidgets import QApplication, QInputDialog
from CODE.GAMEWINDOW import GameWindow
from CODE.player import Player
from CODE.SAVE import SaveManager
from LOGIC.level import Level
from LOGIC.rouge import Rouge

class Game:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = GameWindow()
        self.save_manager = SaveManager()
        self.level_manager = Level()
        self.player = None
        self.current_level = None
        self.current_monster = None
        self.difficulty = None  # Add difficulty attribute
        self.rouge = Rouge()

        # Connect signals from the UI
        self.window.confirm_name_button.clicked.connect(self.handle_name_confirmation)
        self.window.easy_button.clicked.connect(lambda: self.set_difficulty('simple'))
        self.window.normal_button.clicked.connect(lambda: self.set_difficulty('normal'))
        self.window.hard_button.clicked.connect(lambda: self.set_difficulty('hard'))
        self.window.progression_button.clicked.connect(self.show_progression_window)
        self.window.upgrade_health_button.clicked.connect(lambda: self.upgrade_stat('health'))
        self.window.upgrade_attack_button.clicked.connect(lambda: self.upgrade_stat('attack'))
        self.window.upgrade_defense_button.clicked.connect(lambda: self.upgrade_stat('defense'))
        self.window.choice_made.connect(self.handle_choice)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec_())

    def handle_name_confirmation(self):
        player_name = self.window.name_input.text()
        if player_name:
            if self.save_manager.player_exists(player_name):
                self.player = self.save_manager.load_player(player_name)
                self.window.log_message(f'Welcome back, {player_name}!')
            else:
                self.player = Player(player_name)
                self.save_manager.save_player(self.player)
                self.window.log_message(f'Welcome, {player_name}! A new journey begins.')
            self.window.show_difficulty_selection()
        else:
            self.window.log_message("Please enter a name.")

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.window.log_message(f"Difficulty set to {difficulty}.")
        self.start_game()

    def show_progression_window(self):
        if self.player:
            self.update_progression_window()
            self.window.progression_window.show()

    def upgrade_stat(self, stat_name):
        if self.player.upgrade_permanent_stat(stat_name):
            self.save_manager.save_player(self.player)
            self.update_progression_window()
            self.window.update_player_stats(self.player)
            self.window.log_message(f"Upgraded {stat_name}.")
        else:
            self.window.log_message("Not enough soul crystals.")

    def update_progression_window(self):
        self.window.soul_crystals_label.setText(f"Soul Crystals: {self.player.soul_crystals}")
        self.window.progression_health_label.setText(f"Health: {self.player.permanent_health}")
        self.window.progression_attack_label.setText(f"Attack: {self.player.permanent_attack}")
        self.window.progression_defense_label.setText(f"Defense: {self.player.permanent_defense}")

    def start_game(self):
        self.window.show_game_content() # Show the main game UI
        self.player.reset_for_new_game()
        self.window.update_player_stats(self.player)
        self.load_player_art()
        self.start_new_level(1)

    def start_new_level(self, level_id):
        self.current_level = self.level_manager.get_level(self.difficulty, level_id)
        if self.current_level:
            self.current_monster = self.current_level
            self.window.log_message(f"Level {level_id}: A {self.current_monster['monster']} appears!")
            self.window.update_monster_stats(self.current_monster)
            self.load_monster_art()
            self.window.attack_button.clicked.connect(self.player_attack)
        else:
            self.window.log_message('You have completed all levels!')

    def player_attack(self):
        player_damage = self.player.deal_damage()
        monster_defense = self.current_monster['stats']['defense']
        damage_to_monster = max(0, player_damage - monster_defense)
        self.current_monster['stats']['health'] -= damage_to_monster
        self.window.log_message(f"You attacked the {self.current_monster['monster']} for {damage_to_monster} damage.")
        self.window.update_monster_stats(self.current_monster)

        if self.current_monster['stats']['health'] <= 0:
            self.window.log_message(f"You defeated the {self.current_monster['monster']}!")
            self.player.soul_crystals += self.current_monster['reward']
            self.save_manager.save_player(self.player)
            self.present_choices()
            return

        self.monster_attack()

    def present_choices(self):
        choices = self.rouge.get_random_in_game_options(3)
        self.window.show_choices("Choose your buff!", choices)

    def handle_choice(self, choice):
        self.player.apply_in_game_option(choice['name'])
        self.window.hide_choices()
        self.window.log_message(f"You chose: {choice['description']}")
        self.window.update_player_stats(self.player)
        self.start_new_level(self.current_level['id'] + 1)

    def monster_attack(self):
        monster_damage = self.current_monster['stats']['attack']
        damage_to_player = self.player.take_damage(monster_damage)
        self.window.log_message(f"The {self.current_monster['monster']} attacked you for {damage_to_player} damage.")
        self.window.update_player_stats(self.player)

        if self.player.current_health <= 0:
            self.window.log_message('You have been defeated...')
            self.load_dead_player_art()
            # Game over logic here

    def load_player_art(self):
        try:
            with open('c:\\Users\\chinese\\PycharmProjects\\ASCELL-ROUGE\\ART\\CHARACTERS\\player.txt', 'r', encoding='utf-8') as f:
                art = f.read()
                self.window.set_player_art(art)
        except FileNotFoundError:
            self.window.log_message("Player art not found.")

    def load_dead_player_art(self):
        try:
            with open('c:\\Users\\chinese\\PycharmProjects\\ASCELL-ROUGE\\ART\\CHARACTERS\\dead.txt', 'r', encoding='utf-8') as f:
                art = f.read()
                self.window.set_player_art(art)
        except FileNotFoundError:
            self.window.log_message("Dead player art not found.")

    def load_monster_art(self):
        monster_name = self.current_monster['monster']
        art_file = f'c:\\Users\\chinese\\PycharmProjects\\ASCELL-ROUGE\\ART\\MONSTER\\monster{random.randint(1, 7)}.txt'
        try:
            with open(art_file, 'r', encoding='utf-8') as f:
                art = f.read()
                self.window.set_monster_art(art)
        except FileNotFoundError:
            self.window.log_message(f"Art for {monster_name} not found.")

if __name__ == '__main__':
    game = Game()
    game.run()
