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