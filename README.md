# Maze Generator and Solver

This project visualizes how a maze is generated and then solved automatically. It uses a stack-based depth-first search algorithm to create a proper maze and a backtracking solver to find a path from the left opening to the right opening.

## Overview

The program builds a rectangular maze of `R` rows and `C` columns. Each cell stores whether its north wall and east wall still exist, which matches the wall representation described in the assignment.

By default, the maze is a proper maze:

- every cell is reachable
- there is a unique path between any two cells
- the entrance is on the left edge
- the exit is on the right edge

After the maze is generated, the program solves it visually. The current search path is shown in red, dead ends are marked in blue, and the final successful route remains visible in green.

## Features

- Dynamic maze generation with a visible "mouse" eating through walls
- Stack-based DFS maze construction
- Backtracking maze solver
- Left-edge to right-edge path by default
- Optional harder modes with extra cycles
- Difficulty presets in code for different maze sizes and speeds
- Keyboard controls for solving, resetting, and quitting

## How It Works

The program generates and displays a rectangular maze, then solves it automatically from the left-edge entrance to the right-edge exit. It uses random generation to create a proper maze and backtracking to show the search process and the final path.

### Maze Representation

The maze is stored using two wall arrays:

- `north_wall[row][col]`
- `east_wall[row][col]`

If a value is `1`, the wall is present. If it is `0`, the wall has been removed.

### Maze Generation

The generator follows the "mouse eats walls" idea from the assignment:

1. Start with all walls intact.
2. Place the mouse in a random cell.
3. Check neighboring cells that have not been visited.
4. Randomly choose one unvisited neighbor.
5. Remove the wall between the current cell and that neighbor.
6. Push the path onto a stack and continue.
7. When the mouse reaches a dead end, pop the stack and backtrack.
8. Stop when all cells have been visited.

Because each new cell is connected only once during generation, the result is a proper maze with a unique path structure.

### Maze Solving

The solver uses backtracking:

1. Start at the left-edge opening.
2. Check all possible moves where no wall blocks movement.
3. Move to an unvisited neighbor and push it onto the solution stack.
4. If a dead end is reached, pop the stack and backtrack.
5. Continue until the right-edge exit is found.

This process is shown visually:

- red: current explored path
- blue: dead ends
- green: final solution

## Controls

- `SPACE`: start solving after maze generation finishes
- `R`: generate a new maze
- `ESC`: quit the program

## Project Structure

- `main.py`: game loop and state management
- `maze_generator.py`: random maze generation logic
- `maze_solver.py`: backtracking solver
- `maze_renderer.py`: drawing and animation
- `maze_config.py`: colors, sizes, difficulty presets, and settings

## Installation and Running

### Requirements

- Python 3.8 or higher
- `pygame`

### Setup

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
.\venv\Scripts\Activate.ps1
```

If you are using Command Prompt instead of PowerShell:

```bash
venv\Scripts\activate
```

Install `pygame`:

```bash
pip install pygame
```

Run the program:

```bash
python main.py
```

If you want to run it directly with the project virtual environment on Windows:

```bash
.\venv\Scripts\python.exe main.py
```

## Notes

- Higher difficulty levels can optionally add extra broken walls to create cycles.
- Those cycle-enabled modes are bonus behavior beyond the base proper-maze requirement.

## Link for Demo Video

https://www.loom.com/share/01b960faa87a49a3b25df9160facf725
