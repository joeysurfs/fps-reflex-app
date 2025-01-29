import random
import time
import pygame
from target import Target
from highscores import Highscores
from game_mode import GameMode
import math

class Game:
    def __init__(self):
        self.window = None
        self.running = True
        self.current_target = None
        self.target_appear_time = 0
        self.score = 0
        self.clicks = 0
        self.reaction_times = []
        self.state = "mode_select"  # new initial state
        self.current_mode = None
        self.max_clicks = 20  # will be updated based on mode
        self.highscores = Highscores()
        self.input_text = self.highscores.last_player_name
        self.burst_count = 0  # Track targets within burst
        self.burst_center = None  # Track center point for burst group
        self.burst_direction = None  # Track the movement direction (degrees)
        self.burst_speed = None     # Track simulated movement speed
        self.current_group = 0  # Track which group of 3 we're on
        self.countdown_time = None
        self.countdown_start = None

    def generate_target(self):
        if not self.window:
            return

        if self.current_mode == "burst":
            # Determine which group and position within group
            current_group = self.clicks // 3
            position_in_group = self.clicks % 3
            
            # Generate new burst parameters when starting a new group
            if position_in_group == 0:
                self.burst_center = (
                    random.randint(150, self.window.width - 150),
                    random.randint(150, self.window.height - 150)
                )
                self.burst_direction = random.uniform(0, 2 * math.pi)
                self.burst_speed = random.randint(40, 100)
            
            # Calculate position based on group position
            if position_in_group == 0:
                # First target in group is at center
                x, y = self.burst_center
            else:
                # Second and third targets follow the direction
                offset = position_in_group * self.burst_speed
                x = self.burst_center[0] + offset * math.cos(self.burst_direction)
                y = self.burst_center[1] + offset * math.sin(self.burst_direction)
                
                # Add small random variation to non-center targets
                x += random.uniform(-5, 5)
                y += random.uniform(-5, 5)
            
            # Ensure target stays within screen bounds
            x = max(50, min(self.window.width - 50, x))
            y = max(50, min(self.window.height - 50, y))
            
            self.current_target = Target(x, y, 20)
        else:
            # Standard random target generation for other modes
            x = random.randint(30, self.window.width - 30)
            y = random.randint(30, self.window.height - 30)
            self.current_target = Target(x, y, 20)
            
        self.target_appear_time = time.time()

    def start_game(self, mode_key):
        self.current_mode = mode_key
        self.max_clicks = GameMode.get_mode_info(mode_key)["targets"]
        self.reset_game()
        self.state = "countdown"  # Changed from "playing" to "countdown"
        self.countdown_time = 5
        self.countdown_start = time.time()

    def handle_click(self, pos):
        if self.state == "mode_select":
            mode = self.window.get_clicked_mode(pos)
            if mode:
                self.start_game(mode)
            elif self.window.is_clear_scores_clicked(pos):
                self.state = "confirm_clear"
        elif self.state == "confirm_clear":
            if self.window.is_confirm_yes_clicked(pos):
                self.highscores.clear_scores()  # Clear all scores
                self.state = "mode_select"
            elif self.window.is_confirm_no_clicked(pos):
                self.state = "mode_select"
        elif self.state == "menu":
            if self.window.is_button_clicked(pos):
                self.start_game()
            elif self.window.is_clear_button_clicked(pos):
                self.state = "confirm_clear"
        elif self.state == "confirm_clear":
            if self.window.is_confirm_yes_clicked(pos):
                self.highscores.clear_scores()
                self.state = "menu"
            elif self.window.is_confirm_no_clicked(pos):
                self.state = "menu"
        elif self.state == "ended":
            if self.window.is_continue_button_clicked(pos):
                self.state = "name_input"
        elif self.state == "playing" and self.current_target:
            if self.current_target.is_clicked(*pos):
                reaction_time = time.time() - self.target_appear_time
                self.target_clicked(reaction_time)
                if self.clicks >= self.max_clicks:
                    print(f"Game Over! Average reaction time: {self.average_reaction_time():.3f} seconds")
                    self.state = "ended"
                else:
                    self.generate_target()

    def handle_keydown(self, event):
        if self.state == "name_input":
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.highscores.add_score(
                        self.input_text,
                        self.average_reaction_time(),
                        self.current_mode
                    )
                    self.state = "mode_select"
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            else:
                if len(self.input_text) < 15:  # Limit name length
                    if event.unicode.isalnum() or event.unicode.isspace():
                        self.input_text += event.unicode

    def target_clicked(self, reaction_time):
        self.score += 1
        self.clicks += 1
        self.reaction_times.append(reaction_time)

    def average_reaction_time(self):
        if self.clicks == 0:
            return 0
        return sum(self.reaction_times) / self.clicks

    def reset_game(self):
        self.score = 0
        self.clicks = 0
        self.reaction_times = []
        self.state = "mode_select"
        self.burst_count = 0
        self.burst_center = None
        self.burst_direction = None
        self.burst_speed = None
        self.current_group = 0
        self.countdown_time = None
        self.countdown_start = None

    def update(self):
        if self.state == "countdown":
            current_time = time.time()
            elapsed = current_time - self.countdown_start
            self.countdown_time = 5 - int(elapsed)
            
            if self.countdown_time <= 0:
                self.state = "playing"
                self.generate_target()