import random

class MazeSolver:
    def __init__(self, config):
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
        rows, cols = self.maze['rows'], self.maze['cols']
        self.solver_visited = [[False for _ in range(cols)] for _ in range(rows)]
        self.solution_stack = []
        
        current_row, current_col = self.start
        self.solution_stack.append((current_row, current_col))
        self.solver_visited[current_row][current_col] = True
        
        while self.solution_stack:
            current_row, current_col = self.solution_stack[-1]
            
            if (current_row, current_col) == self.end:
                yield ('success', current_row, current_col)
                return
            
            neighbors = self._get_available_moves(current_row, current_col)
            
            unvisited_moves = [(r, c) for r, c in neighbors 
                              if not self.solver_visited[r][c]]
            
            if unvisited_moves:
                next_row, next_col = self._choose_move(unvisited_moves)
                self.solution_stack.append((next_row, next_col))
                self.solver_visited[next_row][next_col] = True
                yield ('move', next_row, next_col)
            else:
                dead_row, dead_col = self.solution_stack.pop()
                yield ('dead_end', dead_row, dead_col)
                
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
        
        if row > 0 and north_wall[row][col] == 0:
            moves.append((row - 1, col))
        
        if row < rows - 1 and north_wall[row + 1][col] == 0:
            moves.append((row + 1, col))
        
        if col > 0 and east_wall[row][col - 1] == 0:
            moves.append((row, col - 1))
        
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
            return moves[0]
        else:
            return moves[0]
    
    def would_left_hand_rule_work(self):
        if not self.maze:
            return False

        current_row, current_col = self.start
        direction = 2 
        seen_states = set()
        
        while (current_row, current_col) != self.end:
            state = (current_row, current_col, direction)
            if state in seen_states:
                return False
            seen_states.add(state)
            moved = False
            for turn in [-1, 0, 1, 2]:
                next_dir = (direction + turn) % 4
                
                possible_moves = self._get_available_moves(current_row, current_col)
                
                if next_dir == 0:    target = (current_row - 1, current_col)   
                elif next_dir == 1:  target = (current_row, current_col + 1)    
                elif next_dir == 2:  target = (current_row + 1, current_col)   
                elif next_dir == 3:  target = (current_row, current_col - 1)   
                
                if target in possible_moves:
                    current_row, current_col = target
                    direction = next_dir
                    moved = True
                    break
            
            if not moved:
                return False
                
        return True