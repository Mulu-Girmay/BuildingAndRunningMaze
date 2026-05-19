
import random

class MazeGenerator:
    def __init__(self, rows, cols, config):
        self.rows = rows
        self.cols = cols
        self.config = config
       
        self.north_wall = None
        self.east_wall = None
        self.visited = None
        self.stack = []
        
        self._reset()
    
    def _reset(self):
        """Initialize all walls intact"""
        self.north_wall = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.east_wall = [[1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.stack = []
    
    def get_maze(self):
        """Return current maze state for other modules"""
        return {
            'north_wall': self.north_wall,
            'east_wall': self.east_wall,
            'rows': self.rows,
            'cols': self.cols,
            'start': getattr(self, 'start', None),
            'end': getattr(self, 'end', None)
        }
    
    def generate(self, start_row=None, start_col=None):
        """
        Generate maze using DFS - THE MOUSE EATS WALLS
        Yields current position for animation
        """
        self._reset()
        
        
        if start_row is None:
            start_row = random.randint(0, self.rows - 1)
            start_col = random.randint(0, self.cols - 1)
        
        self.visited[start_row][start_col] = True
        self.stack.append((start_row, start_col))
        
        while self.stack:
            current_row, current_col = self.stack[-1]
            
            neighbors = self._get_unvisited_neighbors(current_row, current_col)
            
            if neighbors:
                next_row, next_col, direction = random.choice(neighbors)
                self._eat_wall(current_row, current_col, next_row, next_col, direction)
                
                self.visited[next_row][next_col] = True
                self.stack.append((next_row, next_col))
            else:
                self.stack.pop()
            
            yield (current_row, current_col)
        
        # Choose start and end positions
        self._choose_start_end()
        
        # BONUS: Add cycles (1 in 20 chance)
        if self.config.enable_cycles:
            self._add_cycles(probability=self.config.cycle_probability)
    
    def _get_unvisited_neighbors(self, row, col):
        """Find all adjacent cells that haven't been visited"""
        neighbors = []
        
        # Check North (up)
        if row > 0 and not self.visited[row - 1][col]:
            neighbors.append((row - 1, col, 'north'))
        
        # Check South (down)
        if row < self.rows - 1 and not self.visited[row + 1][col]:
            neighbors.append((row + 1, col, 'south'))
        
        # Check West (left)
        if col > 0 and not self.visited[row][col - 1]:
            neighbors.append((row, col - 1, 'west'))
        
        # Check East (right)
        if col < self.cols - 1 and not self.visited[row][col + 1]:
            neighbors.append((row, col + 1, 'east'))
        
        return neighbors
    
    def _eat_wall(self, r1, c1, r2, c2, direction):
        """
        Eat through the wall between two cells
        The mouse removes the barrier!
        """
        if direction == 'north':
            self.north_wall[r1][c1] = 0  # Remove north wall of current
        elif direction == 'south':
            self.north_wall[r2][c2] = 0  # Remove north wall of neighbor
        elif direction == 'west':
            self.east_wall[r1][c1 - 1] = 0  # Remove east wall of left cell
        elif direction == 'east':
            self.east_wall[r1][c1] = 0  # Remove east wall of current
    
    def _choose_start_end(self):
        """Choose start and end positions (can be interior or edges)"""
        if self.config.start_end_type == 'edges':
            # Classic: Left edge to right edge
            self.start = (random.randint(0, self.rows - 1), 0)
            self.end = (random.randint(0, self.rows - 1), self.cols - 1)
            
            # Create openings on edges
            if self.start[0] > 0:
                self.north_wall[self.start[0]][0] = 0
            if self.end[0] < self.rows - 1:
                self.north_wall[self.end[0] + 1][self.end[1]] = 0
        
        elif self.config.start_end_type == 'interior':
            # Challenging: Both inside the maze
            self.start = (
                random.randint(1, self.rows - 2),
                random.randint(1, self.cols - 2)
            )
            self.end = (
                random.randint(1, self.rows - 2),
                random.randint(1, self.cols - 2)
            )
            
            # Ensure start != end
            while self.start == self.end:
                self.end = (
                    random.randint(1, self.rows - 2),
                    random.randint(1, self.cols - 2)
                )
            
            # Create openings for interior cells
            self._create_openings_at_start_end()
    
    def _create_openings_at_start_end(self):
        """Break walls to allow entry/exit from interior positions"""
        directions = ['north', 'south', 'east', 'west']
        
        # For start
        for direction in random.sample(directions, 1):
            self._break_wall_at(self.start[0], self.start[1], direction)
        
        # For end
        for direction in random.sample(directions, 1):
            self._break_wall_at(self.end[0], self.end[1], direction)
    
    def _break_wall_at(self, row, col, direction):
        """Break a specific wall at a cell"""
        if direction == 'north' and row > 0:
            self.north_wall[row][col] = 0
        elif direction == 'south' and row < self.rows - 1:
            self.north_wall[row + 1][col] = 0
        elif direction == 'west' and col > 0:
            self.east_wall[row][col - 1] = 0
        elif direction == 'east' and col < self.cols - 1:
            self.east_wall[row][col] = 0
    
    def _add_cycles(self, probability=0.05):
        """
        BONUS: Randomly eat extra walls to create cycles
        1 in 20 chance (5%) to create cycles that break the shoulder-to-wall rule
        """
        cycles_created = 0
        
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < probability:
                    # Try to eat north wall
                    if row > 0 and self.north_wall[row][col] == 1:
                        self.north_wall[row][col] = 0
                        cycles_created += 1
                    # Try to eat east wall
                    elif col < self.cols - 1 and self.east_wall[row][col] == 1:
                        self.east_wall[row][col] = 0
                        cycles_created += 1
        
        print(f"[Generator] Created {cycles_created} cycles (extra walls eaten)")