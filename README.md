# 🐭 Maze Generator & Solver

An interactive visualization of maze generation using a "mouse eating walls" DFS algorithm and a backtracking solver with red/blue dot visualization.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Team Members](#team-members)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Controls](#controls)
- [Algorithm Details](#algorithm-details)
- [Project Structure](#project-structure)
- [Technical Specifications](#technical-specifications)
- [Bonus Features](#bonus-features)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## 🎯 Overview

This project generates **perfect mazes** (unique path between any two cells) using a stack-based DFS algorithm where a virtual "mouse" eats through walls to connect cells. The solver then finds a path from start to end using backtracking, visually marking the path with **red dots** and dead ends with **blue dots**.

## ✨ Features

- **Dynamic Maze Generation** - Watch the mouse eat through walls in real-time
- **Multiple Difficulty Levels** - Easy, Medium, Hard, and Expert presets
- **Cycle Creation** - Optional random walls eaten (1 in 20 chance) to create cycles
- **Interior Start/End** - Configurable placement (edges or interior cells)
- **Visual Solver** - Red dots show current path, blue dots mark dead ends
- **Adjustable Animation Speed** - Control generation and solving speeds
- **Keyboard Controls** - Reset, solve, quit at any time

## 👥 Team Members & Responsibilities

| Member       | Module              | Responsibilities                                                     |
| ------------ | ------------------- | -------------------------------------------------------------------- |
| **Person 1** | `main.py`           | Game loop, state management, event handling, integration             |
| **Person 2** | `maze_generator.py` | DFS algorithm, wall eating logic, stack backtracking, cycle creation |
| **Person 3** | `maze_solver.py`    | Backtracking solver, pathfinding, dead end detection                 |
| **Person 4** | `maze_renderer.py`  | Graphics, drawing walls/cells, animations, colors                    |
| **Person 5** | `maze_config.py`    | Configuration, constants, difficulty levels, utilities               |

## 🧠 How It Works

### Maze Generation (The Mouse Algorithm)

1. **Start** with all walls intact (complete grid)
2. **Place mouse** in random starting cell
3. **Find unvisited neighbors** - cells with all 4 walls still intact
4. **Choose randomly** and eat through the connecting wall
5. **Push other candidates** onto a stack for later
6. **Repeat** until mouse reaches dead end
7. **Backtrack** by popping stack to find unvisited cells
8. **Finish** when all cells are visited (stack empty)

### Maze Solving (Backtracking)

1. **Start** at green start circle
2. **Check all 4 directions** for open walls
3. **Move randomly** to unvisited cell (red dot)
4. **Push position** onto solution stack
5. **When stuck** (dead end):
   - Mark cell blue
   - Pop stack to backtrack
6. **Continue** until reaching green end circle

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step-by-Step Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/maze-project.git
cd maze-project

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the program
python main.py
```
