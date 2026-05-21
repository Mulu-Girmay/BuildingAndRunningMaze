import sys

import pygame

from maze_config import Colors, MazeConfig
from maze_generator import MazeGenerator
from maze_renderer import MazeRenderer
from maze_solver import MazeSolver


class MazeGame:
    def __init__(self):
        """Initialize game components."""
        self.config = MazeConfig()
        self.generator = None
        self.solver = None
        self.renderer = None
        self.generation_generator = None
        self.solver_generator = None

        # Game state
        self.state = "GENERATING"  
        self.maze = None
        self.mouse_pos = None
        self.solver_state = {
            "active_path": [],
            "dead_ends": [],
            "solution_path": [],
        }
        self.dead_end_cells = []

        # Pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.config.screen_width, self.config.screen_height)
        )
        pygame.display.set_caption("Maze Generator and Solver")
        self.clock = pygame.time.Clock()
        self.running = True

    def initialize_maze(self):
        """Create a new maze and reset animation state."""
        self.generator = MazeGenerator(
            self.config.rows,
            self.config.cols,
            self.config,
        )
        self.solver = MazeSolver(self.config)
        self.renderer = MazeRenderer(self.config)
        self.generation_generator = self.generator.generate()
        self.solver_generator = None

        self.maze = self.generator.get_maze()
        self.state = "GENERATING"
        self.mouse_pos = None
        self.solver_state = {
            "active_path": [],
            "dead_ends": [],
            "solution_path": [],
        }
        self.dead_end_cells = []

    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.state == "IDLE":
                    self.start_solving()
                elif event.key == pygame.K_r:
                    self.initialize_maze()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def start_solving(self):
        """Switch to solving phase."""
        self.state = "SOLVING"
        self.solver.load_maze(self.maze)
        self.dead_end_cells = []
        self.solver_state = {
            "active_path": ([self.maze["start"]] if self.maze["start"] else []),
            "dead_ends": [],
            "solution_path": [],
        }
        self.solver_generator = self.solver.solve()

    def update_generation(self):
        """Update maze generation phase."""
        try:
            self.mouse_pos = next(self.generation_generator)
            self.maze = self.generator.get_maze()
            self.renderer.draw_generation(
                self.screen, self.maze, self.mouse_pos
            )
            self.clock.tick(self.config.gen_speed)
        except StopIteration:
            self.maze = self.generator.get_maze()
            self.state = "IDLE"
            self.renderer.draw_idle(self.screen, self.maze)
            print("Maze generation complete! Press SPACE to solve")

    def update_solving(self):
        """Update maze solving phase."""
        try:
            action, row, col = next(self.solver_generator)

            if action == "move":
                self.solver_state["active_path"] = list(self.solver.solution_stack)
            elif action == "dead_end":
                self.dead_end_cells.append((row, col))
                self.solver_state["dead_ends"] = list(self.dead_end_cells)
                self.solver_state["active_path"] = list(self.solver.solution_stack)
            elif action == "success":
                self.solver_state["solution_path"] = list(self.solver.solution_stack)
                self.solver_state["dead_ends"] = list(self.dead_end_cells)
                print("Maze solved! Press R for new maze, ESC to quit")
                self.state = "COMPLETE"

            self.renderer.draw_solving(
                self.screen, self.maze, self.solver_state
            )
            self.clock.tick(self.config.solve_speed)

        except StopIteration:
            if self.state == "SOLVING":
                print("No solution found! Press R for new maze")
                self.state = "IDLE"

    def run(self):
        """Main game loop with state machine."""
        self.initialize_maze()

        while self.running:
            self.handle_events()

            if self.state == "GENERATING":
                self.update_generation()
            elif self.state == "SOLVING":
                self.update_solving()
            elif self.state == "IDLE":
                self.renderer.draw_idle(self.screen, self.maze)
                self.clock.tick(self.config.idle_speed)
            elif self.state == "COMPLETE":
                self.renderer.draw_solving(self.screen, self.maze, self.solver_state)
                self.clock.tick(self.config.idle_speed)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = MazeGame()
    game.run()
