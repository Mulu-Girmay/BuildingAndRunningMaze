
# Responsibilities: Backtracking algorithm, pathfinding, dead end detection
# Dependencies: maze_config.py


import random

class MazeSolver:
    def init(self, config):
        self.config = config
        self.maze = None
        self.solver_visited = None
        self.solution_stack = None
        self.start = None
        self.end = None
    
    def load_maze(self, maze_data):
        """Load maze from generator output"""
        self.maze = maze_data
        self.start = maze_data['start']
        self.end = maze_data['end']
        self.solver_visited = None
        self.solution_stack = None
    
    def solve(self):
        
        # Solve maze using backtracking algorithm
        # Yields: (action, row, col)
        # action: 'move' (red dot), 'dead_end' (blue dot), 'success'
        # Reset solver state
        rows, cols = self.maze['rows'], self.maze['cols']
        self.solver_visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.solution_stack = []
        
        current_row, current_col = self.start
        self.solution_stack.append((current_row, current_col))
        self.solver_visited[current_row][current_col] = True
        
        while self.solution_stack:
            current_row, current_col = self.solution_stack[-1]
            
            # Check if reached end
            if (current_row, current_col) == self.end:
                yield ('success', current_row, current_col)
                return
            
            # Find possible moves from current cell
            neighbors = self._get_available_moves(current_row, current_col)
            
            # Filter to unvisited cells
            unvisited_moves = [(r, c) for r, c in neighbors 
                              if not self.solver_visited[r][c]]
            
            if unvisited_moves:
                # Move to next cell (RED DOT)
                next_row, next_col = self._choose_move(unvisited_moves)
                self.solution_stack.append((next_row, next_col))
                self.solver_visited[next_row][next_col] = True
                yield ('move', next_row, next_col)
            else:
                # Dead end - backtrack and mark (BLUE DOT)
                dead_row, dead_col = self.solution_stack.pop()
                yield ('dead_end', dead_row, dead_col)
         