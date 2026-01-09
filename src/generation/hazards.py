import random 
from typing import List,Dict,Tuple
from entities.trap import Trap
from entities.agent import Agent

class Hazards:



    # hazards in teh enviroment
    ozone_raditation = "ozone_radiation"
    silicon_rain = "silicon_rain"
    sulphur_dioxide = "sulphur_dioxide"


    # holes in reality will swallow dek 
    break_domain = "break_domain"
    nuke = "nuke" 




class DynamicHazards:



    def __init__(self, hazard_type: str, x: int, y: int, intensity: float = 1.0):

        self.type = hazard_type
        self.x = x
        self.y = y
        self.intensity = intensity  
        self.age = 0  # turns since creation
        self.active = True
        self.affected_tiles = [(x, y)]  # can spread to multiple tiles

        self.growth_rate = random.uniform(0.05, 0.15)  # how fast it evolves
        self.max_intensity = random.uniform(2.0, 5.0)



    def evolve(self, turn: int):
        self.age += 1


        if self.intensity < self.max_intensity:
            self.intensity += self.growth_rate

        if self.type == Hazards.ozone_raditation and self.age % 5 == 0:
            self._spread()

        
        if self.type == Hazards.break_domain or Hazards.nuke:
            self.active = (turn % 10 != 0)



    def _spread(self):
        
           if len(self.affected_tiles) < 5:  # max spread



            x, y = random.choice(self.affected_tiles)
            directions = [(0,1), (1,0), (0,-1), (-1,0)]
            dx, dy = random.choice(directions)
            new_tile = (x + dx, y + dy)
            if new_tile not in self.affected_tiles:
                self.affected_tiles.append(new_tile)
    

    def get_damage(self) -> int:


        base_damage = {
            Hazards.silicon_rain: 15,
            Hazards.ozone_raditation: 50,
            Hazards.sulphur_dioxide: 10,
            Hazards.break_domain: 999,
            Hazards.nuke : 999
            
        }

        return int(base_damage.get(self.type, 10) * self.intensity)
    



    def affects_position(self, x: int, y: int) -> bool:
        """see if a position is affected by this hazard"""
        return (x, y) in self.affected_tiles and self.active
    










    #---------------------------------------------------------------------------------#




class HazardGenerator:
    """Generates procedural hazards that evolve during runtime"""
    
    def __init__(self, grid_width: int, grid_height: int):
        self.width = grid_width
        self.height = grid_height
        self.hazards: List[DynamicHazards] = []
        self.generation_rate = 0.15  # 15% chance per turn to spawn new hazard
        self.max_concurrent_hazards = 8
        





    def generate_initial_hazards(self, count: int = 3):
        for _ in range(count):
            hazard_type = random.choice([
                Hazards.silicon_rain,
                Hazards.ozone_raditation,
                Hazards.sulphur_dioxide,
            ])
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            
            hazard = DynamicHazards(hazard_type, x, y)
            self.hazards.append(hazard)
            
        print(f"Generated {count} initial hazards")






        
    def update(self, turn: int, difficulty_multiplier: float = 1.0):
        """Update all hazards and potentially spawn new ones"""
        
        # Evolve existing hazards
        for hazard in self.hazards:
            hazard.evolve(turn)
            
        # Remove old hazards that have decayed
        self.hazards = [h for h in self.hazards if h.age < 50]
        
        # Spawn new hazards based on difficulty
        if len(self.hazards) < self.max_concurrent_hazards:
            spawn_chance = self.generation_rate * difficulty_multiplier
            if random.random() < spawn_chance:
                self._spawn_random_hazard(turn)
                
    def _spawn_random_hazard(self, turn: int):
        """Spawn a new hazard at random location"""
        hazard_types = [
             Hazards.silicon_rain,
            Hazards.ozone_raditation,
            Hazards.sulphur_dioxide,
]
        
        # Later turns can spawn more dangerous hazards
        if turn > 30:
            hazard_types.append(Hazards.nuke and Hazards.break_domain)
            
        hazard_type = random.choice(hazard_types)
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        
        intensity = 1.0 + (turn / 100.0)  # scales with time
        hazard = DynamicHazards(hazard_type, x, y, intensity)
        self.hazards.append(hazard)
        
        print(f"New hazard spawned: {hazard_type} at ({x}, {y})")
        
    def check_hazard_damage(self, agent: Agent) -> Tuple[bool, int, str]:
        """
        Check if agent is in a hazard and return (hit, damage, hazard_type)
        """
        for hazard in self.hazards:
            if hazard.affects_position(agent.x, agent.y):
                damage = hazard.get_damage()
                return (True, damage, hazard.type)
                
        return (False, 0, "")
        
    def get_hazards_at(self, x: int, y: int) -> List[DynamicHazards]:

        return [h for h in self.hazards if h.affects_position(x, y)]