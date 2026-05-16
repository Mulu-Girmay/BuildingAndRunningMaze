# Maze Generator and Solver

A visualization of maze generation using DFS "mouse eating" algorithm and backtracking solver.

## How It Works

### Generation

- Starts with all walls intact
- "Mouse" randomly chooses unvisited cells
- Eats walls to connect cells
- Uses stack for backtracking (LIFO)
- Results in a perfect maze (unique path between any two cells)

### Solving

- Backtracking algorithm with visual feedback
- Red dot = current path
- Blue dot = dead end (backtracked)
- Green circles = start and end points

## Running the Program

```bash
python main.py
```
