# Clonix - A Pygame-based Tetris Clone

## Overview
Clonix is a Tetris-like game built using the Pygame library. The game offers standard Tetris gameplay with customized visual assets, where you can rotate and move pieces (tetrominoes) to fill rows and score points. It features dynamic piece-dropping speed, a fading text effect for game-over messages, and support for custom block images.

![clonix_start](https://github.com/user-attachments/assets/bb7a144f-dcbb-4846-b633-e0713852c85f)

## Features
- Tetris-style gameplay with 7 distinct tetromino shapes (S, Z, I, O, J, L, T).
- Increasing difficulty as the player progresses.
- Support for custom images for tetrominoes, with colored blocks as fallback.
- Fade-out text effect when the player loses.
- Menu interface for starting a new game.
- Play-again prompt after game over.
- High score tracking.

## How to Play
1. Launch the game by running the script: `python3 clonix.py`.
2. Move pieces left or right using the arrow keys.
3. Rotate pieces using the UP arrow key.
4. Press DOWN to accelerate the piece’s fall.
5. Complete rows to score points. The game ends when the tetrominoes pile up to the top of the screen.
6. After a game over, choose to play again or quit.

## Controls
- **LEFT ARROW**: Move piece to the left.
- **RIGHT ARROW**: Move piece to the right.
- **DOWN ARROW**: Drop the piece faster.
- **UP ARROW**: Rotate the piece clockwise.

![clonix_start](https://github.com/user-attachments/assets/1a5de1d1-b435-4504-bd59-bb0dd93f9f2a)

![game](https://github.com/user-attachments/assets/6fcea4c1-d778-4923-88c5-cbba0da9d121)


## Dependencies

To run Clonix on Debian/Ubuntu-based systems, you need to install Python and Pygame. Use the following commands to install the required dependencies:

## Install Python and Pygame

```bash
sudo apt install python3-pygame 

sudo apt install python3-pillow ```   

- python-pillow is only needed if legacy/intitial_scripts are used to generate the very basic style. 
```

## Optional: Image Assets

The game comes with support for custom images for the tetromino blocks. You can place PNG images for the shapes (S.png, Z.png, I.png, O.png, J.png, L.png, T.png) in the assets folder. If images are not found, the game will fall back to using colored blocks for each shape.

## Running the Game

After installing the dependencies, clone the repository or copy the code to your local machine, and run the game with the following command:

```bash 

python3 clonix.py```
```

<b> Notice since this is the first version of this game, some bugs might exist. Report them back if you find them. </b>

## License

This project is licensed under the GNU General Public License v2.0. See the LICENSE file for more details.

Copyright (c) 2024 JJ Posti <techtimejourney.net>

This program comes with ABSOLUTELY NO WARRANTY; for details see: GNU GPL.
This is free software, and you are welcome to redistribute it under GPL Version 2, June 1991.
