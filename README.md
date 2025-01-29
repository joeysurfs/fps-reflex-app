# README.md

# FPS Reflex Application

This project is a simple target practice game implemented in Python. The objective of the game is to click on randomly generated circles on the screen, with the average reaction time displayed after each playthrough.

![example-test](https://github.com/user-attachments/assets/1c609356-82d7-4571-b926-8c77eb635c10)

Compete for the highest score in 4 different game modes that will test your precision and coordination.

## Game Modes

### 10 Target, 20 Target, 50 Target
Randomly generated targets that spawn a new random target when clicked with the mouse cursor. Click through the selected amount of targets to calculate an average reaction time and compete for the high score.

#### Example:
![example-test](https://github.com/user-attachments/assets/cb1d6fba-4b0b-423e-9cae-f5e35b25c7d7)

### Burst - 30 Target
Similar to the previous game modes, however these targets are more procedurely generated. **EVERY THREE TARGETS** will be generated on a random line on the X and Y axes varying in small distances from each other. The goal is to simulate FPS movement and practice smaller precision.  

#### Example:
![burst-example](https://github.com/user-attachments/assets/d8732ea2-058e-488f-bafd-56954cba7721)

## Leaderboards

After each round, the user's reaction time is displayed and allows the user to input a 10 character name for their highscore. The leaderboard will make note of the date so that users can track their progress.

All scores can be cleared within the main menu.

#### Example:
![leaderboard-example](https://github.com/user-attachments/assets/c0d86de2-3955-4827-a0e5-467a4a80500e)



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
