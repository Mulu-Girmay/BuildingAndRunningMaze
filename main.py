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
        self.state = "GENERATING"  # GENERATING, SOLVING, IDLE, COMPLETE
        self.maze = None
        self.mouse_pos = None
        self.solver_state = []
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
        self.solver_state = []
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
        self.solver_state = (
            [(self.maze["start"], Colors.RED)] if self.maze["start"] else []
        )
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
                self.solver_state = self._build_solver_state(Colors.RED)
            elif action == "dead_end":
                self.dead_end_cells.append((row, col))
                self.solver_state = self._build_solver_state(Colors.RED)
            elif action == "success":
                self.solver_state = self._build_solver_state(Colors.GREEN)
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

    def _build_solver_state(self, active_color):
        """Compose the active path together with confirmed dead ends."""
        solver_state = [((row, col), Colors.BLUE) for row, col in self.dead_end_cells]
        solver_state.extend(
            (position, active_color) for position in self.solver.solution_stack
        )
        return solver_state

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
