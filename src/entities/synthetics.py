import sys
from entities.agent import Agent
from core.grid import Grid
from entities.monster import Monster


class Synthetic(Agent):
    
    def __init__(self, x, y, name="Synthetic", isThia=False):

        symbol = "T" if isThia else 'S'
        super().__init__(x, y, symbol, name)


        self.stamina = 100
        self.max_stamina = 100
        self.isThia = isThia
        self.isDamaged = False

    def judge_damage(self):
        if self.isThia:
            if self.health < 50:
                self.isDamaged = False
                print("Thia is damaged and must be carried!")
                return False
        else: return None


    def scan_area(self, grid: Grid, scan_range=3):
        scan_results = {
            'monsters': [],
            'predators': [],
            'synthetics': [],
            'boss': None,
            'threats_detected': 0,
            'thia': None
    }
        
        # Scan in a square around Thia's position
        for dx in range(-scan_range, scan_range + 1):
            for dy in range(-scan_range, scan_range + 1):
                # Skip Thia's own position
                if dx == 0 and dy == 0:
                    continue
                
                check_x = self.x + dx
                check_y = self.y + dy
                
                cell_content = grid.get_cell(check_x, check_y)
                
                if cell_content is not None:
                    # Check what type of agent it is
                    if isinstance(cell_content, Monster):
                        monster_info = {
                            'name': cell_content.name,
                            'position': (check_x % grid.width, check_y % grid.height),
                            'distance': abs(dx) + abs(dy),
                            'health': cell_content.health,
                            'is_boss': cell_content.is_boss
                        }
                        
                        if cell_content.is_boss:
                            scan_results['boss'] = monster_info
                        else:
                            scan_results['monsters'].append(monster_info)
                    
                    elif isinstance(cell_content, Predator):
                        predator_info = {
                            'name': cell_content.name,
                            'position': (check_x % grid.width, check_y % grid.height),
                            'distance': abs(dx) + abs(dy),
                            'is_dek': cell_content.isDek
                        }
                        scan_results['predators'].append(predator_info)
                    
                    elif isinstance(cell_content, Synthetic):
                        synthetic_info = {
                            'name': cell_content.name,
                            'position': (check_x % grid.width, check_y % grid.height),
                            'distance': abs(dx) + abs(dy),
                            'health': cell_content.health,
                            'is_thia': cell_content.isThia
                        }
                        
                        if cell_content.isThia:
                            scan_results['thia'] = synthetic_info  # ← Was 'predator_info' - wrong!
                        else:
                            scan_results['synthetics'].append(synthetic_info)
    
        return  scan_results# ← Must be aligned with first 'for' loop


                    



                

grid = Grid(20,20)
thia = Synthetic(5, 5, "Thia")
thia.scan_area(grid, scan_range=2) 


        