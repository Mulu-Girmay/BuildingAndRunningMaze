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