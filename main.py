import sys
import pygame
import configparser
from game import Game  # Main game logic
from display import Display  # Pygame display
from leaderboards import Leaderboards  # Leaderboards handling

# Config loading
config = configparser.ConfigParser()
config.read('config.ini')
board_width = int(config['BoardSettings']['Width'])
board_height = int(config['BoardSettings']['Height'])
initial_automove_interval = int(config['GameSettings']['AutoMoveInterval'])
start_music = config['Assets']['StartMusic']
game_music = config['Assets']['GameMusic']
gameover_music = config['Assets']['GameOverMusic']
volume = float(config['WindowSettings']['Volume'])
constant_move_interval = int(config['GameSettings']['ConstantMoveInterval'])
auto_move_base = float(config['GameSettings']['AutoMoveBase'])

# Pygame initialization
pygame.init()
leaderboards = Leaderboards()
display = Display()


def mute_unmute():
    if pygame.mixer.music.get_volume() == 0:
        pygame.mixer.music.set_volume(volume)
    else:
        pygame.mixer.music.set_volume(0)


def start_game():
    last_moves_timestamps = {
        'down': pygame.time.get_ticks(),
        'left': pygame.time.get_ticks(),
        'right': pygame.time.get_ticks()
    }

    game = Game(board_width, board_height)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(game_music)
    pygame.mixer.music.play(-1, fade_ms=750)

    return 1, game, last_moves_timestamps


# Handling input from player
def handle_input(scene, game=None, timestamps=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leaderboards.save()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if display.quit_button is not None and display.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            if display.music_button is not None and display.music_button.collidepoint(event.pos):
                mute_unmute()

        if scene == 0:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if display.play_button is not None and display.play_button.collidepoint(event.pos):
                    return start_game()

        elif scene == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                    timestamps['right'] = pygame.time.get_ticks()
                elif event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                    timestamps['left'] = pygame.time.get_ticks()
                elif event.key == pygame.K_UP:
                    game.rotate(1)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                    timestamps['down'] = pygame.time.get_ticks()
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                    timestamps['down'] = pygame.time.get_ticks()
                elif event.key == pygame.K_c:
                    game.hold()
                elif event.key == pygame.K_z:
                    game.rotate(-1)

        elif scene == 2:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if display.play_button is not None and display.play_button.collidepoint(event.pos):
                    return start_game()

    return scene, game, timestamps


# Handling continuous input (when key is kept press down) for smooth tetrominoes movement
def handle_continuous_input(game, timestamps, interval=constant_move_interval):
    pressed_keys = pygame.key.get_pressed()

    if pressed_keys[pygame.K_DOWN] and pygame.time.get_ticks() - timestamps['down'] >= interval:
        game.move(0, 1)
        timestamps['down'] = pygame.time.get_ticks()
    if pressed_keys[pygame.K_LEFT] and pygame.time.get_ticks() - timestamps['left'] >= interval:
        game.move(-1, 0)
        timestamps['left'] = pygame.time.get_ticks()
    if pressed_keys[pygame.K_RIGHT] and pygame.time.get_ticks() - timestamps['right'] >= interval:
        game.move(1, 0)
        timestamps['right'] = pygame.time.get_ticks()


def main():
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(start_music)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1)

    # 0 - starting screen; 1 - main game; 2 - game over screen
    scene_id = 0

    while True:
        if scene_id == 0:
            display.update(scene_id)
            scene_id, game, last_moves_timestamps = handle_input(0)

        elif scene_id == 1:
            # Auto moving a piece
            automove_interval = initial_automove_interval * (auto_move_base) ** (game.level)
            if pygame.time.get_ticks() - last_moves_timestamps['down'] >= automove_interval:
                game.move(0, 1)
                last_moves_timestamps['down'] = pygame.time.get_ticks()

            handle_continuous_input(game, last_moves_timestamps)
            scene_id, game, last_moves_timestamps = handle_input(1, game, last_moves_timestamps)

            display.update(scene_id, game=game)

            # Go to game over screen if player lost
            if game.game_over:
                leaderboards.add_score(game.score)
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(gameover_music)
                pygame.mixer.music.play(-1, fade_ms=750)
                scene_id = 2


        elif scene_id == 2:
            display.update(scene_id, game=game, scores=leaderboards.highestscores)
            scene_id, game, last_moves_timestamps = handle_input(2, game)

        clock.tick(60)


if __name__ == '__main__':
    main()
