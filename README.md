# Dino Game

A simple 2D game built with Pygame where the player controls a dinosaur that must jump and crouch to avoid obstacles. The game features scrolling ground, animated sprites, and increasing difficulty as the score goes up.

## Features

- **Scrolling Ground:** The ground continuously moves to simulate forward motion.
- **Dino Control:** Jump and crouch to avoid obstacles.
- **Obstacles:** Includes birds and trees that the dino must avoid.
- **Scoring System:** Points are awarded for surviving, and the game speed increases with the score.
- **Sound Effects:** Includes sounds for jumping, scoring, and game over.

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/techiuv/dino-pyhon-game.git
    cd dino-python-game
    ```

2. **Install Pygame:**

    Ensure you have Python installed. Then install Pygame using pip:

    ```bash
    pip install pygame
    ```

3. **Download Assets:**

    Make sure to add the following assets to the `assets` directory:
    - `ground.png`
    - `font.ttf`
    - `dino1.png`
    - `dino2.png`
    - `dino_crouch1.png`
    - `dino_crouch2.png`
    - `bird1.png`
    - `bird2.png`
    - `tree1.png` to `tree5.png`
    - `dead.mp3`
    - `jump.mp3`
    - `points.mp3`

4. **Run the Game:**

    Execute the game script using Python:

    ```bash
    python main.py
    ```

## Controls

- **Spacebar:** Jump/Crouch
- **Restart:** Spacebar when game over

## Contributing

Feel free to fork the repository and submit pull requests. If you find any issues or have suggestions for improvements, please open an issue on the GitHub repository.

## Acknowledgments

- **Pygame:** For providing the framework to build the game.
- **OpenGameArt.org:** For some of the assets used in the game.

