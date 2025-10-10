import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QGridLayout, QLineEdit
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import pyqtSignal

class GameWindow(QWidget):
    choice_made = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle('ASCEL ROUGE')
        self.setGeometry(100, 100, 1200, 800)
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.main_layout = QHBoxLayout()

        # --- Name Input Layout (Initially Visible) ---
        self.name_input_layout = QVBoxLayout()
        self.name_label = QLabel("Enter your name:")
        self.name_input = QLineEdit()
        self.confirm_name_button = QPushButton("Confirm")
        self.name_input_layout.addWidget(self.name_label)
        self.name_input_layout.addWidget(self.name_input)
        self.name_input_layout.addWidget(self.confirm_name_button)
        self.main_layout.addLayout(self.name_input_layout)

        # --- Difficulty Selection Layout (Initially Hidden) ---
        self.difficulty_layout = QVBoxLayout()
        self.difficulty_label = QLabel("Select Difficulty:")
        self.easy_button = QPushButton("Easy")
        self.normal_button = QPushButton("Normal")
        self.hard_button = QPushButton("Hard")
        self.difficulty_layout.addWidget(self.difficulty_label)
        self.difficulty_layout.addWidget(self.easy_button)
        self.difficulty_layout.addWidget(self.normal_button)
        self.difficulty_layout.addWidget(self.hard_button)
        # Initially hide the difficulty selection
        self.difficulty_widget = QWidget()
        self.difficulty_widget.setLayout(self.difficulty_layout)
        self.difficulty_widget.setVisible(False)
        self.main_layout.addWidget(self.difficulty_widget)


        # --- Game Content Layout (Initially Hidden) ---
        self.game_content_widget = QWidget()
        game_content_layout = QHBoxLayout()


        # Left side - Message Log and Actions (Information Area)
        info_area_layout = QVBoxLayout()

        # Message Log
        self.message_log = QTextEdit()
        self.message_log.setReadOnly(True)
        self.message_log.setFont(QFont('Arial', 12))
        info_area_layout.addWidget(self.message_log)

        # Action buttons
        self.action_layout = QGridLayout()
        self.attack_button = QPushButton('Attack')
        self.skill_button_1 = QPushButton('Skill 1')
        self.skill_button_2 = QPushButton('Skill 2')
        self.skill_button_3 = QPushButton('Skill 3')
        self.progression_button = QPushButton('Character Progression') # Add progression button
        self.action_layout.addWidget(self.attack_button, 0, 0)
        self.action_layout.addWidget(self.skill_button_1, 1, 0)
        self.action_layout.addWidget(self.skill_button_2, 1, 1)
        self.action_layout.addWidget(self.skill_button_3, 1, 2)
        self.action_layout.addWidget(self.progression_button, 0, 1, 1, 2) # Add to layout
        info_area_layout.addLayout(self.action_layout)

        # --- In-Game Choice Layout (Initially Hidden) ---
        self.choice_layout = QVBoxLayout()
        self.choice_label = QLabel("Choose your reward:")
        self.choice_layout.addWidget(self.choice_label)
        self.choice_widget = QWidget()
        self.choice_widget.setLayout(self.choice_layout)
        self.choice_widget.setVisible(False)
        info_area_layout.addWidget(self.choice_widget)

        # --- Progression Window (Initially Hidden) ---
        self.progression_window = QWidget()
        self.progression_window.setWindowTitle("Character Progression")
        progression_layout = QVBoxLayout()
        self.soul_crystals_label = QLabel("Soul Crystals: 0")
        self.upgrade_health_button = QPushButton("Upgrade Health (Cost: 10)")
        self.upgrade_attack_button = QPushButton("Upgrade Attack (Cost: 10)")
        self.upgrade_defense_button = QPushButton("Upgrade Defense (Cost: 10)")
        progression_layout.addWidget(self.soul_crystals_label)
        progression_layout.addWidget(self.upgrade_health_button)
        progression_layout.addWidget(self.upgrade_attack_button)
        progression_layout.addWidget(self.upgrade_defense_button)
        self.progression_window.setLayout(progression_layout)


        # Right side - Player and Monster Info (Art Area)
        art_area_layout = QHBoxLayout()

        # Player Area
        player_layout = QVBoxLayout()
        # Player Art
        self.player_art_label = QLabel('Player Art')
        self.player_art_label.setFont(QFont('Courier New', 10))
        self.player_art_label.setFixedSize(400, 300)
        player_layout.addWidget(self.player_art_label)

        # Player Stats
        self.player_stats_label = QLabel('Player Stats:')
        self.player_stats_label.setFont(QFont('Arial', 14))
        player_layout.addWidget(self.player_stats_label)
        self.player_stats_grid = QGridLayout()
        self.player_health_label = QLabel('Health:')
        self.player_attack_label = QLabel('Attack:')
        self.player_defense_label = QLabel('Defense:')
        self.player_stats_grid.addWidget(self.player_health_label, 0, 0)
        self.player_stats_grid.addWidget(self.player_attack_label, 1, 0)
        self.player_stats_grid.addWidget(self.player_defense_label, 2, 0)
        player_layout.addLayout(self.player_stats_grid)
        art_area_layout.addLayout(player_layout)

        # Monster Area
        monster_layout = QVBoxLayout()
        # Monster Art
        self.monster_art_label = QLabel('Monster Art')
        self.monster_art_label.setFont(QFont('Courier New', 10))
        self.monster_art_label.setFixedSize(400, 300)
        monster_layout.addWidget(self.monster_art_label)

        # Monster Stats
        self.monster_stats_label = QLabel('Monster Stats:')
        self.monster_stats_label.setFont(QFont('Arial', 14))
        monster_layout.addWidget(self.monster_stats_label)
        self.monster_stats_grid = QGridLayout()
        self.monster_name_label = QLabel('Name:')
        self.monster_health_label = QLabel('Health:')
        self.monster_attack_label = QLabel('Attack:')
        self.monster_defense_label = QLabel('Defense:')
        self.monster_stats_grid.addWidget(self.monster_name_label, 0, 0)
        self.monster_stats_grid.addWidget(self.monster_health_label, 1, 0)
        self.monster_stats_grid.addWidget(self.monster_attack_label, 2, 0)
        self.monster_stats_grid.addWidget(self.monster_defense_label, 3, 0)
        monster_layout.addLayout(self.monster_stats_grid)
        art_area_layout.addLayout(monster_layout)

        # Add info and art areas to game content layout
        game_content_layout.addLayout(info_area_layout)
        game_content_layout.addLayout(art_area_layout)

        self.game_content_widget.setLayout(game_content_layout)
        self.game_content_widget.setVisible(False) # Initially hide the game content
        self.main_layout.addWidget(self.game_content_widget)


        self.setLayout(self.main_layout)

    def show_choices(self, choices):
        # Clear previous choices
        for i in reversed(range(1, self.choice_layout.count())):
            self.choice_layout.itemAt(i).widget().setParent(None)

        for choice in choices:
            button = QPushButton(choice['name'])
            button.clicked.connect(lambda _, c=choice: self.choice_made.emit(c))
            self.choice_layout.addWidget(button)

        self.choice_widget.setVisible(True)

    def hide_choices(self):
        self.choice_widget.setVisible(False)

    def show_difficulty_selection(self):
        # Hide name input
        for i in range(self.name_input_layout.count()):
            self.name_input_layout.itemAt(i).widget().setVisible(False)
        # Show difficulty selection
        self.difficulty_widget.setVisible(True)

    def show_game_content(self):
        # Hide difficulty selection
        self.difficulty_widget.setVisible(False)
        # Show game content
        self.game_content_widget.setVisible(True)


    def log_message(self, message):
        self.message_log.append(message)
        self.message_log.moveCursor(QTextCursor.End)

    def update_player_stats(self, player):
        self.player_health_label.setText(f'Health: {player.current_health}/{player.health}')
        self.player_attack_label.setText(f'Attack: {player.current_attack}')
        self.player_defense_label.setText(f'Defense: {player.current_defense}')

    def update_monster_stats(self, monster):
        self.monster_name_label.setText(monster['monster'])
        self.monster_health_label.setText(f'Health: {monster["stats"]["health"]}')
        self.monster_attack_label.setText(f'Attack: {monster["stats"]["attack"]}')
        self.monster_defense_label.setText(f'Defense: {monster["stats"]["defense"]}')

    def set_player_art(self, art):
        self.player_art_label.setText(art)

    def set_monster_art(self, art):
        self.monster_art_label.setText(art)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameWindow()
    window.show()
    sys.exit(app.exec_())
