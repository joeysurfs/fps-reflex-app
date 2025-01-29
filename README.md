# README.md

# FPS Reflex Application

This project is a simple target practice game implemented in Python. The objective of the game is to click on randomly generated circles on the screen, with the average reaction time displayed after each playthrough.

![example-test](https://github.com/user-attachments/assets/1c609356-82d7-4571-b926-8c77eb635c10)

Compete for the highest score in 4 different game modes that will test your precision and coordination.

## Game Modes

### 10 Target
(Randomly generated)
### 20 Target
(Randomly generated)
### Burst - 30 Target
(Simulates random FPS movement)
### 50 Target
(Randomly generated)

#### Example:
![example-test](https://github.com/user-attachments/assets/cb1d6fba-4b0b-423e-9cae-f5e35b25c7d7)

## Project Structure

```
fps-reflex-app
├── src
│   ├── main.py          # Entry point of the application
│   ├── game.py          # Game logic and state management
│   ├── target.py        # Target representation and click detection
│   └── ui
│       └── window.py    # User interface handling
├── tests
│   ├── __init__.py      # Marks the tests directory as a package
│   ├── test_game.py     # Unit tests for the Game class
│   └── test_target.py    # Unit tests for the Target class
└── requirements.txt      # Project dependencies
highscores.json       # Highscore management
README.md             # Project documentation
```

## Requirements

To run this project, you need to have Python installed along with the required dependencies. You can install the dependencies using:

```
pip install -r requirements.txt
```

## Running the Game

To start the game, run the following command:

```
python src/main.py
```

Enjoy the game and try to improve your reaction time!
