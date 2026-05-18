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