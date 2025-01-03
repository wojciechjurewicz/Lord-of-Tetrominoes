
# Lord Of Tetrominoes 

Medival themed Tetris game made in PyGame for Algorithms And Data Models course


## Authors

- **Wojciech Jurewicz** index no. 250382

## Controls

- **Arrow Keys**: Move the tetrominoes (left, right, down).
- **Up Arrow**: Rotate the tetromino clockwise.
- **Spacebar**: Hard drop (instantly drop the tetromino).
- **Z**: Rotate the tetromino counterclockwise.
- **C**: Hold the current tetromino for later use.


## Features

- **Core Gameplay Mechanics**: Includes falling tetrominoes, line clearing, and classic Tetris rules.
- **Tetromino Queue**: Displays upcoming pieces to prepare for the next move.
- **Hold Piece**: Option to store a tetromino for later use.
- **Super Rotation System**: Smooth piece rotation with proper handling of edge and corner collisions.
- **Hard Drop**: Instantly drop the tetromino to the bottom of the screen.
- **Continuous Movement**: Tetrominoes move as long as the key is held down.
- **Ghost Piece**: Visual indicator of where the current piece will land.
- **Dynamic Difficulty**: Game difficulty increases over time based on the level.
- **Leaderboards**: Tracking and saving high scores in a file.
- **Fullscreen Mode**: Play in fullscreen with automatic resolution scaling.
- **Clickable buttons**: Buttons for muting the sound, exiting, or starting a new game.
- **Help button**: Button displaying in-game controls.
- **Comprehensive UI with Graphics**: Includes a starting screen, active game screen with score and next pieces, and a game over screen. Comes with background graphics and block textures.
- **Music**: In-game music, different for all screens.
## Acknowledgements

 - Graphics and textures made using DALL-E
- [Starting screen music](https://www.youtube.com/watch?v=dYootbp7pDs)
- [Game music](https://www.youtube.com/watch?v=YmcdaiwGGXs)
- [Game over music](https://youtu.be/jJSa1D-Inw0?si=3jE6obUtAo_Kx8Dt)
- [Rules for Tetrominoes rotation](https://harddrop.com/wiki/SRS)
## Repository

You can find the project repository on [GitHub](https://github.com/wojciechjurewicz/Lord-of-Tetrominoes).

## Run Locally

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the game

```bash
  python main.py
```

