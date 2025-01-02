import sys
import pygame
from game import Game
from display import Display
import configparser
from leaderboards import Leaderboards

config = configparser.ConfigParser()
config.read('config.ini')
board_width = int(config['BoardSettings']['Width'])
board_height = int(config['BoardSettings']['Height'])
initial_automove_interval = int(config['GameSettings']['AutoMoveInterval'])
start_music = config['Assets']['StartMusic']
game_music = config['Assets']['GameMusic']
gameover_music = config['Assets']['GameOverMusic']

pygame.init()

leaderboards = Leaderboards()
display = Display()

def change_volume():
    if pygame.mixer.music.get_volume() == 0:
        pygame.mixer.music.set_volume(1)
    else:
        pygame.mixer.music.set_volume(0)

def handle_input(game, last_move_time):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            leaderboards.save()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                game.move(0, 1)
                last_move_time = pygame.time.get_ticks()
            elif event.key == pygame.K_RIGHT:
                game.move(1, 0)
            elif event.key == pygame.K_LEFT:
                game.move(-1, 0)
            elif event.key == pygame.K_UP:
                game.rotate(1)
            elif event.key == pygame.K_SPACE:
                game.hard_drop()
                last_move_time = pygame.time.get_ticks()
            elif event.key == pygame.K_c:
                game.hold()
            elif event.key == pygame.K_z:
                game.rotate(-1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if display.quit_button is not None and display.quit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            if display.music_button is not None and display.music_button.collidepoint(event.pos):
                change_volume()


    return last_move_time

def main():
    clock = pygame.time.Clock()
    pygame.mixer.init()
    pygame.mixer.music.load(start_music)
    pygame.mixer.music.play(-1)
    # 0 - starting screen; 1 - main game; 2 - game over screen
    scene_id = 0
    while True:
        if scene_id == 0:
            display.update(scene_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    leaderboards.save()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if display.quit_button is not None and display.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
                    if display.play_button is not None and display.play_button.collidepoint(event.pos):
                        last_move_time = pygame.time.get_ticks()
                        game = Game(board_width, board_height)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play(-1, fade_ms=750)
                        scene_id = 1
                    if display.music_button is not None and display.music_button.collidepoint(event.pos):
                        change_volume()

        elif scene_id == 1:
            automove_interval = initial_automove_interval * (0.9) ** (game.level)
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= automove_interval:
                game.move(0, 1)
                last_move_time = pygame.time.get_ticks()
            last_move_time = handle_input(game, last_move_time)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    leaderboards.save()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if display.quit_button is not None and display.quit_button.collidepoint(event.pos):
                        leaderboards.save()
                        pygame.quit()
                        sys.exit()
                    if display.play_button is not None and display.play_button.collidepoint(event.pos):
                        last_move_time = pygame.time.get_ticks()
                        del game
                        game = Game(board_width, board_height)
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load(game_music)
                        pygame.mixer.music.play(-1)
                        scene_id = 1
                    if display.music_button is not None and display.music_button.collidepoint(event.pos):
                        change_volume()

        clock.tick(30)

if __name__ == '__main__':
    main()