import pygame
from maze_config import Colors

class MazeRenderer:
    def init(self, config):
        self.config = config
        self.cell_size = config.cell_size
        
        # Cache for performance optimization
        self._wall_cache = {}
        self._dirty = True
    
    def draw_generation(self, screen, maze_data, mouse_pos=None):
        """Draw maze during generation phase (with mouse)"""
        self._draw_maze_base(screen, maze_data)
        
        # Draw mouse (red dot)
        if mouse_pos:
            self._draw_circle(
                screen, 
                mouse_pos[0], mouse_pos[1], 
                Colors.RED, 
                self.config.cell_size // 3
            )
        
        pygame.display.flip()
    
    def draw_solving(self, screen, maze_data, solver_state):
        """Draw maze during solving phase (red/blue dots)"""
        self._draw_maze_base(screen, maze_data)
        
        # Draw solver state (red/blue dots)
        if solver_state:
            for (row, col), color in solver_state:
                self._draw_circle(
                    screen, row, col, 
                    color, 
                    self.config.cell_size // 3
                )
        
        pygame.display.flip()
    
    def draw_idle(self, screen, maze_data):
        """Draw maze in idle state (no mouse, no solver)"""
        self._draw_maze_base(screen, maze_data)
        pygame.display.flip()
    
    def _draw_maze_base(self, screen, maze_data):
        """Draw the complete maze structure (walls and start/end)"""
        north_wall = maze_data['north_wall']
        east_wall = maze_data['east_wall']
        rows = maze_data['rows']
        cols = maze_data['cols']
        start = maze_data['start']
        end = maze_data['end']
        
        screen.fill(Colors.BLACK)
        cs = self.cell_size
        
        # Draw all cells (optimized with minimal operations)
        for row in range(rows):
            for col in range(cols):
                x = col * cs
                y = row * cs
                
                # Draw north wall
                if north_wall[row][col]:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x, y), (x + cs, y), 2
                    )
                
                # Draw east wall
                if east_wall[row][col]:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x + cs, y), (x + cs, y + cs), 2
                    )
                
                # Draw west wall (left edge of maze)
                if col == 0:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x, y), (x, y + cs), 2
                    )
                
                # Draw south wall (bottom edge of maze)
                if row == rows - 1:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x, y + cs), (x + cs, y + cs), 2
                    )
        
        # Draw start and end (green circles)
        if start:
            self._draw_circle(screen, start[0], start[1], Colors.GREEN, cs // 3)
        if end:
            self._draw_circle(screen, end[0], end[1], Colors.GREEN, cs // 3)
    
    def _draw_circle(self, screen, row, col, color, radius):
        """Draw a circle centered in a cell"""
        cs = self.cell_size
        center_x = col * cs + cs // 2
        center_y = row * cs + cs // 2
        pygame.draw.circle(screen, color, (center_x, center_y), radius)
    
    def draw_text(self, screen, text, x, y, color=Colors.WHITE):
        """Draw text overlay (for instructions)"""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    
    def clear_cache(self):
        """Clear drawing cache (when maze changes)"""
        self._wall_cache = {}
        self._dirty = True

    
