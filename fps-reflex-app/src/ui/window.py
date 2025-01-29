import pygame
import os
from game_mode import GameMode

class GameWindow:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = self.screen.get_size()  # Get actual screen size
        pygame.display.set_caption("Target Practice Game")
        self.clock = pygame.time.Clock()
        pygame.font.init()
        
        # Try arcade-style system fonts in order of preference
        font_names = ['Consolas', 'Courier New', 'Lucida Console', 'Monaco']
        
        # Find first available monospace font
        selected_font = None
        selected_font_name = None
        for font_name in font_names:
            try:
                selected_font = pygame.font.SysFont(font_name, 36, bold=True)  # Bold for arcade feel
                selected_font_name = font_name
                break
            except:
                continue
                
        # Fallback to default if no system fonts work
        if not selected_font:
            selected_font = pygame.font.Font(None, 36)
            selected_font_name = None
            
        self.font = selected_font
        self.title_font = pygame.font.SysFont(selected_font_name if selected_font_name else None, 56, bold=True)  # Larger size for title
        self.button_font = pygame.font.SysFont(selected_font_name if selected_font_name else None, 32, bold=True)  # Smaller font for buttons
        self.countdown_font = pygame.font.SysFont(selected_font_name if selected_font_name else None, 120, bold=True)  # Countdown font
            
        # Standard button dimensions as instance variables
        self.button_width = 400
        self.button_height = 60
        self.button_spacing = 40
        
        # Update all button rectangles with new width
        self.button_rect = pygame.Rect(
            width//2 - self.button_width//2,
            height//2 - self.button_height//2,
            self.button_width,
            self.button_height
        )
        
        self.continue_button_rect = pygame.Rect(
            width//2 - self.button_width//2,
            height//2 + 50,
            self.button_width,
            self.button_height
        )
        
        # Clear button using same dimensions
        self.clear_button_rect = pygame.Rect(
            width//2 - self.button_width//2,
            height - 150,
            self.button_width,
            self.button_height
        )
        
        self.confirm_yes_rect = pygame.Rect(width//2 - 160, height//2 + 20, 120, 40)
        self.confirm_no_rect = pygame.Rect(width//2 + 40, height//2 + 20, 120, 40)
        self.input_text = ""
        self.input_active = False

        # Create mode selection buttons with new dimensions - position on right side
        self.mode_buttons = {}
        button_section_width = self.width // 3  # Right third of screen
        button_x = self.width - button_section_width + (button_section_width - self.button_width) // 2
        y_pos = height//2 - 150  # Start higher up to accommodate all buttons
        
        for mode_key, mode_info in GameMode.get_all_modes().items():
            self.mode_buttons[mode_key] = pygame.Rect(
                button_x,
                y_pos,
                self.button_width,
                self.button_height
            )
            y_pos += self.button_height + self.button_spacing

        # Add padding for leaderboard layout
        self.leaderboard_padding = 20
        self.score_height = 25  # Height per score entry

        # Add clear scores button at bottom of screen
        self.clear_scores_button = pygame.Rect(
            width//2 - self.button_width//2,
            height - 100,  # Position near bottom
            self.button_width,
            self.button_height
        )

    def update_display(self, game_state, targets, remaining_targets=0, max_targets=0, avg_reaction_time=0, highscores=None, input_text="", current_mode=None, countdown_time=None):
        self.screen.fill((0, 0, 0))  # Changed from white to black
        
        if game_state == "menu":
            # Draw start button
            pygame.draw.rect(self.screen, (0, 255, 0), self.button_rect)
            text = self.font.render("Start", True, (0, 0, 0))
            text_rect = text.get_rect(center=self.button_rect.center)
            self.screen.blit(text, text_rect)
            
            # Draw leaderboard
            if highscores and highscores.get_top_scores():
                # Draw title
                title = self.title_font.render("Top 10 Scores:", True, (255, 255, 255))
                title_rect = title.get_rect(center=(self.width//2, 50))
                self.screen.blit(title, title_rect)
                
                # Draw scores with ranking numbers
                for i, score in enumerate(highscores.get_top_scores(10)):
                    date_str = score.get('date', 'N/A')  # Fallback for old scores
                    score_text = f"#{i+1}. {score['name']}: {score['time']:.3f}s ({date_str})"
                    text = self.font.render(score_text, True, (255, 255, 255))
                    text_rect = text.get_rect(center=(self.width//2, 120 + i * 40))
                    self.screen.blit(text, text_rect)
                    
            # Draw clear leaderboard button with smaller font
            pygame.draw.rect(self.screen, (255, 50, 50), self.clear_button_rect)
            clear_text = self.button_font.render("Clear Scores", True, (0, 0, 0))
            clear_rect = clear_text.get_rect(center=self.clear_button_rect.center)
            self.screen.blit(clear_text, clear_rect)

        elif game_state == "name_input":
            # Draw name input field
            prompt = self.font.render("Enter your name:", True, (255, 255, 255))
            self.screen.blit(prompt, (self.width//2 - 100, self.height//2 - 100))
            
            input_bg = pygame.Rect(self.width//2 - 100, self.height//2 - 50, 200, 40)
            pygame.draw.rect(self.screen, (255, 255, 255), input_bg)
            
            text_surface = self.font.render(input_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (input_bg.x + 5, input_bg.y + 5))
            
            instruction = self.font.render("Press ENTER to submit", True, (255, 255, 255))
            self.screen.blit(instruction, (self.width//2 - 100, self.height//2 + 20))
            
        elif game_state == "ended":
            # Draw score text
            score_text = f"Average Reaction Time: {avg_reaction_time:.3f} seconds"
            text = self.font.render(score_text, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width//2, self.height//2 - 50))
            self.screen.blit(text, text_rect)
            
            # Draw continue button
            pygame.draw.rect(self.screen, (0, 255, 0), self.continue_button_rect)
            continue_text = self.font.render("Continue", True, (0, 0, 0))
            continue_rect = continue_text.get_rect(center=self.continue_button_rect.center)
            self.screen.blit(continue_text, continue_rect)

        elif game_state == "confirm_clear":
            # Draw confirmation dialog
            # Title
            title = self.title_font.render("Clear All Leaderboards?", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width//2, self.height//2 - 80))
            self.screen.blit(title, title_rect)
            
            # Warning message
            warning = self.font.render("This action cannot be undone!", True, (255, 50, 50))
            warning_rect = warning.get_rect(center=(self.width//2, self.height//2 - 20))
            self.screen.blit(warning, warning_rect)

            # Yes/No buttons
            button_configs = [
                (self.confirm_yes_rect, "Yes", (255, 50, 50)),  # Red for warning
                (self.confirm_no_rect, "No", (100, 100, 100))   # Grey for cancel
            ]
            
            for rect, text, color in button_configs:
                pygame.draw.rect(self.screen, color, rect)
                button_text = self.button_font.render(text, True, (0, 0, 0))
                text_rect = button_text.get_rect(center=rect.center)
                self.screen.blit(button_text, text_rect)

        elif game_state == "mode_select":
            # Draw title
            title = self.title_font.render("FPS Reflex Practice", True, (255, 255, 255))
            title_rect = title.get_rect(center=(self.width//2, 50))
            self.screen.blit(title, title_rect)

            # Draw mode buttons on right side
            for mode_key, button_rect in self.mode_buttons.items():
                mode_info = GameMode.get_mode_info(mode_key)
                pygame.draw.rect(self.screen, (0, 255, 0), self.mode_buttons[mode_key])
                mode_text = mode_info['name']
                text = self.button_font.render(mode_text, True, (0, 0, 0))
                text_rect = text.get_rect(center=self.mode_buttons[mode_key].center)
                self.screen.blit(text, text_rect)

            # Draw all leaderboards in left two-thirds of screen
            leaderboard_width = (2 * self.width) // 3 - self.leaderboard_padding * 2
            top_modes = ["quick", "normal"]
            bottom_modes = ["burst", "extended"]
            
            # Top row leaderboards
            x_pos = self.leaderboard_padding
            y_pos = 120
            self._draw_leaderboard_row(x_pos, y_pos, top_modes, highscores, leaderboard_width)

            # Bottom row leaderboards
            y_pos = self.height // 2
            self._draw_leaderboard_row(x_pos, y_pos, bottom_modes, highscores, leaderboard_width)

            # Draw clear scores button at bottom
            pygame.draw.rect(self.screen, (255, 50, 50), self.clear_scores_button)
            clear_text = self.button_font.render("Clear All Leaderboards", True, (0, 0, 0))
            clear_rect = clear_text.get_rect(center=self.clear_scores_button.center)
            self.screen.blit(clear_text, clear_rect)

        elif game_state == "countdown":
            # Draw countdown text
            if countdown_time is not None:
                countdown_text = str(countdown_time)
                text = self.countdown_font.render(countdown_text, True, (255, 255, 255))
                text_rect = text.get_rect(center=(self.width//2, self.height//2))
                self.screen.blit(text, text_rect)
                
                # Draw "Get Ready!" text
                ready_text = self.font.render("Get Ready!", True, (255, 255, 255))
                ready_rect = ready_text.get_rect(center=(self.width//2, self.height//2 - 100))
                self.screen.blit(ready_text, ready_rect)
                
                # Draw selected mode
                if current_mode:
                    mode_info = GameMode.get_mode_info(current_mode)
                    mode_text = self.font.render(mode_info['name'], True, (255, 255, 255))
                    mode_rect = mode_text.get_rect(center=(self.width//2, self.height//2 + 100))
                    self.screen.blit(mode_text, mode_rect)

        else:
            # Draw targets
            for target in targets:
                pygame.draw.circle(self.screen, (255, 0, 0), (target.x, target.y), target.size)
            
            # Draw target counter with white text for better visibility on black
            counter_text = f"Targets: {remaining_targets}/{max_targets}"  # Changed from max_targets - remaining_targets
            text = self.font.render(counter_text, True, (255, 255, 255))
            self.screen.blit(text, (10, 10))
        
        pygame.display.flip()

    def _draw_leaderboard_column(self, x_pos, y_pos, modes, highscores):
        """Helper method to draw a column of leaderboards"""
        for mode_key in modes:
            mode_info = GameMode.get_mode_info(mode_key)
            scores = highscores.get_top_scores(mode_key, 5)  # Show top 5 for each mode
            
            # Draw mode title
            title = self.font.render(f"{mode_info['name']} - Top Scores:", True, (255, 255, 255))
            self.screen.blit(title, (x_pos, y_pos))
            y_pos += 35

            # Draw scores
            if scores:
                for i, score in enumerate(scores):
                    score_text = f"#{i+1}. {score['name']}: {score['time']:.3f}s ({score.get('date', 'N/A')})"
                    text = self.button_font.render(score_text, True, (255, 255, 255))
                    self.screen.blit(text, (x_pos + 20, y_pos))
                    y_pos += self.score_height
            else:
                text = self.button_font.render("No scores yet", True, (255, 255, 255))
                self.screen.blit(text, (x_pos + 20, y_pos))
            
            y_pos += 40  # Add space between different mode leaderboards

    def _draw_leaderboard_row(self, x_pos, y_pos, modes, highscores, total_width):
        """Helper method to draw a row of leaderboards"""
        width_per_board = total_width // len(modes)
        
        for i, mode_key in enumerate(modes):
            mode_info = GameMode.get_mode_info(mode_key)
            scores = highscores.get_top_scores(mode_key, 5)
            
            # Draw mode title
            title = self.font.render(f"{mode_info['name']} - Top Scores:", True, (255, 255, 255))
            self.screen.blit(title, (x_pos + i * width_per_board, y_pos))
            
            # Draw scores
            if scores:
                for j, score in enumerate(scores):
                    score_text = f"#{j+1}. {score['name']}: {score['time']:.3f}s ({score.get('date', 'N/A')})"
                    text = self.button_font.render(score_text, True, (255, 255, 255))
                    self.screen.blit(text, (x_pos + i * width_per_board + 20, y_pos + 35 + j * self.score_height))
            else:
                text = self.button_font.render("No scores yet", True, (255, 255, 255))
                self.screen.blit(text, (x_pos + i * width_per_board + 20, y_pos + 35))

    def handle_mouse_click(self, pos):
        return pos  # Return the position of the mouse click

    def is_button_clicked(self, pos):
        return self.button_rect.collidepoint(pos)

    def is_continue_button_clicked(self, pos):
        return self.continue_button_rect.collidepoint(pos)

    def is_clear_button_clicked(self, pos):
        return self.clear_button_rect.collidepoint(pos)

    def is_confirm_yes_clicked(self, pos):
        return self.confirm_yes_rect.collidepoint(pos)

    def is_confirm_no_clicked(self, pos):
        return self.confirm_no_rect.collidepoint(pos)

    def get_clicked_mode(self, pos):
        for mode_key, button_rect in self.mode_buttons.items():
            if button_rect.collidepoint(pos):
                return mode_key
        return None

    def is_clear_scores_clicked(self, pos):
        return self.clear_scores_button.collidepoint(pos)

    def close(self):
        pygame.quit()