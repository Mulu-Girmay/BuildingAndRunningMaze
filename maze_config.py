class Colors:
    """Color constants for maze visualization"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    GRAY = (128, 128, 128)
    PURPLE = (128, 0, 128)
class Difficulty:
    """Difficulty presets"""
    EASY = {
        'rows': 10,
        'cols': 15,
        'cell_size': 40,
        'gen_speed': 60,   # Fast generation
        'solve_speed': 20,  # Slow solving
        'enable_cycles': False,
        'cycle_probability': 0.0
    }
    
    MEDIUM = {
        'rows': 15,
        'cols': 20,
        'cell_size': 30,
        'gen_speed': 30,
        'solve_speed': 15,
        'enable_cycles': False,
        'cycle_probability': 0.0
    }
    
    HARD = {
        'rows': 20,
        'cols': 30,
        'cell_size': 25,
        'gen_speed': 20,
        'solve_speed': 10,
        'enable_cycles': True,  # Cycles make it harder!
        'cycle_probability': 0.05
    }
    
    EXPERT = {
        'rows': 25,
        'cols': 35,
        'cell_size': 20,
        'gen_speed': 15,
        'solve_speed': 8,
        'enable_cycles': True,
        'cycle_probability': 0.10  # More cycles
    }

class MazeConfig:
    def __init__(self, difficulty='MEDIUM'):
        self.set_difficulty(difficulty)
        self.start_end_type = 'interior'  # 'edges' or 'interior'  
        self.solver_strategy = 'random'  # 'random', 'prefer_right', 'prefer_left'      
        self.show_instructions = True
        self.animation_enabled = True
    
    def set_difficulty(self, difficulty):
        """Change difficulty level"""
        levels = {
            'EASY': Difficulty.EASY,
            'MEDIUM': Difficulty.MEDIUM,
            'HARD': Difficulty.HARD,
            'EXPERT': Difficulty.EXPERT
        }
        
        settings = levels.get(difficulty.upper(), Difficulty.MEDIUM)
        
        self.rows = settings['rows']
        self.cols = settings['cols']
        self.cell_size = settings['cell_size']
        self.gen_speed = settings['gen_speed']
        self.solve_speed = settings['solve_speed']
        self.enable_cycles = settings['enable_cycles']
        self.cycle_probability = settings['cycle_probability']
        
        self.screen_width = self.cols * self.cell_size + 10
        self.screen_height = self.rows * self.cell_size + 10
        self.idle_speed = 60
    
    def get_info(self):
        """Return configuration info for display"""
        return {
            'size': f"{self.rows} x {self.cols}",
            'cycles': "Enabled" if self.enable_cycles else "Disabled",
            'start_end': self.start_end_type,
            'solver': self.solver_strategy
        }

class Stack:
    """Stack implementation for backtracking (LIFO)"""
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

class Queue:
   
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        self.items.insert(0, item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)

def compare_stack_vs_queue():
   
    return "Stack is better for proper mazes with unique paths"

def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))

def distance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])