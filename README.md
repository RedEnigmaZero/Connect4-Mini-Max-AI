# Connect 4 AI

This project is a Python-based Connect 4 game that allows a human to play against various AI agents or for AI agents to compete against each other. It features a Pygame-based GUI, time-limited moves, and several AI implementations, including Minimax, Alpha-Beta Pruning, and Monte Carlo.

## Features

* Playable Connect 4 game engine.
* GUI visualization using Pygame.
* Console-based play option.
* Time limits for player moves to ensure fair competition.
* Multiple AI and human player types:
    * **Human (GUI)**: `humanGUI`
    * **Human (Console)**: `humanConsole`
    * **Random AI**: `randomAI`
    * **Simple AI**: `stupidAI` (plays a fixed, simple strategy)
    * **Minimax AI**: `minimaxAI`
    * **Alpha-Beta Pruning AI**: `alphaBetaAI`
    * **Monte Carlo AI**: `monteCarloAI`

## Dependencies

The project requires the following Python libraries:

* `pygame`
* `numpy`

You can install them using pip:

```bash
pip install pygame numpy
```

## How to Run

The main entry point for the project is main.py. You can run the game from your terminal using python and specify the players and other options as command-line arguments.

```bash
python main.py -p1 <player1_agent> -p2 <player2_agent> [options]
```

### Player Agents

Use the following keys for the -p1 and -p2 arguments:

- humanGUI
- humanConsole
- stupidAI
- randomAI
- monteCarloAI
- minimaxAI
- alphaBetaAI
