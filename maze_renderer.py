import pygame
from maze_config import Colors

class MazeRenderer:
    def __init__(self, config):
        self.config = config
        self.cell_size = config.cell_size
        
        self._wall_cache = {}
        self._dirty = True
    
    def draw_generation(self, screen, maze_data, mouse_pos=None):
        """Draw maze during generation phase (with mouse)"""
        self._draw_maze_base(screen, maze_data)
        
        if mouse_pos:
            self._draw_circle(
                screen, 
                mouse_pos[0], mouse_pos[1], 
                Colors.RED, 
                self.config.cell_size // 3
            )
        
        pygame.display.flip()
    
    def draw_solving(self, screen, maze_data, solver_state):
        """Draw maze during solving phase (red/blue/green dots)"""
        self._draw_maze_base(screen, maze_data)
        
        if solver_state:
            if isinstance(solver_state, dict):
                for row, col in solver_state.get("active_path", []):
                    self._draw_circle(
                        screen, row, col,
                        Colors.RED,
                        self.config.cell_size // 3,
                    )

                for row, col in solver_state.get("solution_path", []):
                    self._draw_circle(
                        screen, row, col,
                        Colors.GREEN,
                        self.config.cell_size // 3,
                    )

                for row, col in solver_state.get("dead_ends", []):
                    self._draw_dead_end_marker(screen, row, col)
            else:
                for (row, col), color in solver_state:
                    if color == Colors.BLUE:
                        self._draw_dead_end_marker(screen, row, col)
                    else:
                        self._draw_circle(
                            screen, row, col,
                            color,
                            self.config.cell_size // 3
                        )
        
        pygame.display.flip()
    
    def draw_idle(self, screen, maze_data):
        self._draw_maze_base(screen, maze_data)
        pygame.display.flip()
    
    def _draw_maze_base(self, screen, maze_data):
        north_wall = maze_data['north_wall']
        east_wall = maze_data['east_wall']
        rows = maze_data['rows']
        cols = maze_data['cols']
        start_end_type = maze_data.get('start_end_type', 'edges')
        start = maze_data['start']
        end = maze_data['end']
        
        screen.fill(Colors.BLACK)
        cs = self.cell_size
        
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
                draw_east_wall = east_wall[row][col]
                if (
                    start_end_type == 'edges'
                    and end
                    and col == cols - 1
                    and row == end[0]
                ):
                    draw_east_wall = 0

                if draw_east_wall:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x + cs, y), (x + cs, y + cs), 2
                    )
                
                # Draw west wall
                draw_west_wall = col == 0
                if (
                    start_end_type == 'edges'
                    and start
                    and col == 0
                    and row == start[0]
                ):
                    draw_west_wall = False

                if draw_west_wall:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x, y), (x, y + cs), 2
                    )
                
                # Draw south wall 
                if row == rows - 1:
                    pygame.draw.line(
                        screen, Colors.WHITE,
                        (x, y + cs), (x + cs, y + cs), 2
                    )
        
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

    def _draw_dead_end_marker(self, screen, row, col):
        """Draw a more visible blue marker for dead ends."""
        cs = self.cell_size
        center_x = col * cs + cs // 2
        center_y = row * cs + cs // 2
        outer_radius = max(6, cs // 2 - 3)
        inner_radius = max(3, outer_radius - 4)

        pygame.draw.circle(
            screen,
            Colors.WHITE,
            (center_x, center_y),
            outer_radius,
        )
        pygame.draw.circle(
            screen,
            Colors.BLUE,
            (center_x, center_y),
            inner_radius,
        )
    
    def draw_text(self, screen, text, x, y, color=Colors.WHITE):
        """Draw text overlay (for instructions)"""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))
    
    def clear_cache(self):
        """Clear drawing cache (when maze changes)"""
        self._wall_cache = {}
        self._dirty = True

    
