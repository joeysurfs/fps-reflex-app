import pygame
from game import Game
from ui.window import GameWindow

def main():
    pygame.init()
    
    # Get the current screen resolution
    info = pygame.display.Info()
    window = GameWindow(info.current_w, info.current_h)
    
    game = Game()
    game.window = window
    game.generate_target()
    
    while game.running:
        game.update()  # Add update call for countdown
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.running = False
                else:
                    game.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.handle_click(pygame.mouse.get_pos())
        
        window.update_display(
            game.state,
            [game.current_target] if game.current_target else [],
            game.clicks,
            game.max_clicks,
            game.average_reaction_time(),
            game.highscores,
            game.input_text,
            game.current_mode,
            game.countdown_time  # Add countdown time parameter
        )
        window.clock.tick(60)

    window.close()

if __name__ == "__main__":
    main()