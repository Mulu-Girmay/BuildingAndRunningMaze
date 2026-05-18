
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
                
                # No solution found
        yield ('failed', None, None)
    
    def _get_available_moves(self, row, col):
        """
        Get all cells reachable from current cell
        Checks north_wall and east_wall arrays
        """
        north_wall = self.maze['north_wall']
        east_wall = self.maze['east_wall']
        rows = self.maze['rows']
        cols = self.maze['cols']
        
        moves = []
        
        # Check North (up)
        if row > 0 and north_wall[row][col] == 0:
            moves.append((row - 1, col))
        
        # Check South (down)
        if row < rows - 1 and north_wall[row + 1][col] == 0:
            moves.append((row + 1, col))
        
        # Check West (left)
        if col > 0 and east_wall[row][col - 1] == 0:
            moves.append((row, col - 1))
        
        # Check East (right)
        if col < cols - 1 and east_wall[row][col] == 0:
            moves.append((row, col + 1))
        
        return moves
    
    def _choose_move(self, moves):
        """
        Choose next move
        Can be random or deterministic (for different solving styles)
        """
        if self.config.solver_strategy == 'random':
            return random.choice(moves)
        elif self.config.solver_strategy == 'prefer_right':
            # Right-hand rule (for comparison with left-hand rule)
            return moves[0]  # Simplified - would need direction tracking
        else:
            return moves[0]
    
         