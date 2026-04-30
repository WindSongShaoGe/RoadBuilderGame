<<<<<<< HEAD
# Road Builder Game - Logical Road Building Puzzle

A Python + Pygame implementation of a logical road building puzzle game, designed for Task 1 coursework.

## Game Features

- **4x4 Grid Game Board**: Based on Task 1's 4 road builders concept
- **4 Challenge Levels**: Increasing difficulty
- **Road/Bridge Pieces**: Various types including horizontal, vertical, turns, bridges, and ramps
- **Vehicle Animation**: Vehicle follows the path when solution is found
- **Cost-based Scoring**: Score based on construction cost (like the reference video)
- **Path Finding**: BFS algorithm to validate solutions

## Requirements

```bash
pip install pygame
```

## How to Run

```bash
cd road_builder_game
python main.py
```

## Controls

- **Mouse Click**: Select and place road pieces
- **Number Keys (1-9)**: Quick select pieces
- **RUN Button**: Start vehicle simulation
- **RESET Button**: Reset current level
- **ESC**: Return to menu

## Game Mechanics

1. Select a piece from the right panel
2. Click on grid cells to place pieces
3. Connect the path from START (green) to END (red)
4. Click RUN to test your solution
5. Lower cost = higher score!

## Challenge Levels

| Level | Name | Difficulty |
|-------|------|------------|
| 1 | Basic Road | Easy |
| 2 | The Gap | Medium |
| 3 | Maze Runner | Hard |
| 4 | The Challenge | Expert |

## Evaluation Criteria Mapping

This implementation covers Task 1 requirements:

- ✅ Core Mechanics: Vehicle moves from start to end
- ✅ Challenge Support: 4 distinct challenges
=======
<<<<<<< HEAD
# Road Builder Game

A Logical Road Builder puzzle game with physics simulation, built with Python and Pygame.

## Game Description

Players build bridges and roads to help vehicles travel from start to destination. The game features a realistic physics system - bridges must be structurally sound for vehicles to pass safely.

## Features

- 4 challenging levels with increasing difficulty
- Physics-based bridge building system
- Cost-based scoring system (lower cost = higher score)
- Vehicle animation when solution is found
- Clean GUI interface

## Requirements

```
pip install pygame
```

## How to Play

1. Select a challenge level
2. Build bridges/roads by clicking on the grid
3. Click "Start" to test if the vehicle can pass
4. Score is calculated based on construction cost

## Controls

- **Left Click**: Place/remove road components
- **Start Button**: Test your solution
- **Reset Button**: Reset current challenge
- **Level Select**: Choose different challenges

## Evaluation Criteria Met

- ✅ Core Mechanics: Vehicle moves from start to end over placed components
- ✅ Challenge Support: 4 distinct challenges included
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
- ✅ Correct Accessory Placement Logic
- ✅ Vehicle Animation
- ✅ Win Detection
- ✅ GUI Layout Clarity
- ✅ Visual Feedback
<<<<<<< HEAD
- ✅ Code Organization (classes/functions)
- ✅ Comments and Naming

## Bonus Features

- Cost-based scoring system (inspired by the reference video)
- Visual piece preview on hover
- Direction indicators on vehicle

## File Structure

```
road_builder_game/
├── main.py          # Main game code
└── README.md        # This file
```

## Author

Created for Computer Science Foundation Coursework - Task 1
=======
- ✅ Code Organization with classes
=======
# RoadBuilderGame
Logical Road Builder Game with Physics - A puzzle game where players build bridges for vehicles to cross
>>>>>>> bb303cab62b15ca2e1bb514629d83fe757d91ec8
>>>>>>> f56e601d65e2c24e33985b9b1302c9416529a868
