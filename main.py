"""
PERSON 1: Game Loop & Integration
Responsibilities: Main loop, event handling, state management
Dependencies: All other modules
"""

import pygame
import sys
from maze_config import MazeConfig, Colors
from maze_generator import MazeGenerator
from maze_solver import MazeSolver
from maze_renderer import MazeRenderer

class MazeGame:
    def __init__(self):
        """Initialize game components"""
        self.config = MazeConfig()
        self.generator = None
        self.solver = None
        self.renderer = None
        
        # Game state
        self.state = 'GENERATING'  # GENERATING, SOLVING, IDLE, COMPLETE
        self.maze = None
        self.mouse_pos = None
        self.solver_state = []
        self.path_history = []
        
        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.config.screen_width, self.config.screen_height)
        )
        pygame.display.set_caption("Maze Generator and Solver")
        self.clock = pygame.time.Clock()
        self.running = True
    
    def initialize_maze(self):
        """Create new maze instance"""
        from maze_generator import MazeGenerator
        self.generator = MazeGenerator(
            self.config.rows, 
            self.config.cols,
            self.config
        )
        self.solver = MazeSolver(self.config)
        self.renderer = MazeRenderer(self.config)
        
        self.maze = self.generator.get_maze()
        self.state = 'GENERATING'
        self.mouse_pos = None
        self.solver_state = []
        self.path_history = []
    
    def handle_events(self):
        """Process all input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == 'IDLE':
                    self.start_solving()
                elif event.key == pygame.K_r:  # Reset maze
                    self.initialize_maze()
                elif event.key == pygame.K_ESCAPE:  # Quit
                    self.running = False
    
    def start_solving(self):
        """Switch to solving phase"""
        self.state = 'SOLVING'
        self.solver.load_maze(self.maze)
        self.solver_state = []
        self.path_history = []
        self.solver_generator = self.solver.solve()
    
    def update_generation(self):
        """Update maze generation phase"""
        try:
            self.mouse_pos = next(self.generator.generate())
            self.renderer.draw_generation(
                self.screen, self.maze, self.mouse_pos
            )
            self.clock.tick(self.config.gen_speed)
        except StopIteration:
            self.state = 'IDLE'
            self.renderer.draw_idle(self.screen, self.maze)
            print("Maze generation complete! Press SPACE to solve")
    
    def update_solving(self):
        """Update maze solving phase"""
        try:
            action, row, col = next(self.solver_generator)
            
            if action == 'move':
                self.path_history.append((row, col))
                self.solver_state = [
                    (pos, Colors.RED) for pos in self.path_history[-30:]
                ]
            elif action == 'dead_end':
                self.solver_state.append(((row, col), Colors.BLUE))
            elif action == 'success':
                self.solver_state = [(pos, Colors.GREEN) for pos in self.path_history]
                print("✓ MAZE SOLVED! Press R for new maze, ESC to quit")
                self.state = 'COMPLETE'
            
            self.renderer.draw_solving(
                self.screen, self.maze, self.solver_state
            )
            self.clock.tick(self.config.solve_speed)
            
        except StopIteration:
            if self.state == 'SOLVING':
                print("✗ No solution found! Press R for new maze")
                self.state = 'IDLE'
    
    def run(self):
        """Main game loop with state machine"""
        self.initialize_maze()
        
        while self.running:
            self.handle_events()
            
            if self.state == 'GENERATING':
                self.update_generation()
            elif self.state == 'SOLVING':
                self.update_solving()
            elif self.state in ['IDLE', 'COMPLETE']:
                self.renderer.draw_idle(self.screen, self.maze)
                self.clock.tick(self.config.idle_speed)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MazeGame()
    game.run()