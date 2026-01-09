from entities.agent import Agent
from entities.synthetics import Synthetic
from core.grid import Grid
class Predator(Agent):
    
   
     

    def __init__(self,x,y,name = "Predator", isDek = False,role = 'Warrior'):
        
        symbol = 'D' if isDek else 'P'
        super().__init__(x,y,symbol,name)

        self.stamina = 100
        self.maxStamina = 100
        self.honour = 50
        self.isDek = isDek
        self.role = role
        self.dek_relationship = 0 
        self.respect_threshhold = 50
        self.trophies = []
        self.carrying_target = None

        #whats he doing and whats he done >:)
        self.kills = 0 
        self.loadCarrying = 0
        self.encumbered = False
        self.carrying_target = None
        self.weapon_damage_buff = 0
        self.inventory = []
        self.max_inventory = 3


        if isDek:
            from ai.reinforcement import Qlearning
            self.q_learner = Qlearning()
            self.current_state = None
            self.last_action = None
            print(f"{name} initialized with Q-learning AI.")

        grid = Grid()
        

    def challenge_dek(self, dek, grid):
        dek_position = abs(self.x - dek.x) + abs(self.y - dek.y)

        status = self.get_clan_status(dek)

        if dek_position > 2:
            return False
        


        if self.name == "Father":
            if status == "EXILE":
                print(f"\n⚔️  {self.name}: 'You dishonour the cla{dek.name}! Prove yourself or die little man!'")
                self.dek_relationship -= 10
                return True
            elif status == "DISAPPROVED":
                print(f"\n  {self.name}: 'You have {dek.kills} kills and {dek.honour} honour LOCK IN AND PROVE YOUR WORTH!'")
                self.dek_relationship -= 5
                return True
            elif status == "ACCEPTED":
                print(f"\n✓ {self.name}: 'Well done {dek.name}. You have proven yourself, good job son.'")
                self.dek_relationship += 5
                return True
        
        #brother challengeds dek
        elif self.name == "Brother":
            if dek.kills > self.kills + 2:
                print(f"\n  {self.name}: 'Your {dek.kills} kills make you arrogant, Dek! I only have {self.kills}!  :( )'")
                self.dek_relationship -= 5
                return True
            elif status == "ACCEPTED" and dek.honour > self.honour:
                print(f"\n  {self.name}: 'You may have {dek.honour} honour but I am still superior! HAHAHA!'")
                self.dek_relationship -= 3
                return True
            elif status == "DISAPPROVED":
                print(f"\n  {self.name}: 'Still weak scared little man brother.'")
                return True
        
        return False
            


        

        
        
        
        


    def useStamina(self,ammount):

        if self.stamina >= ammount:
            self.stamina -= ammount
            return True
        else:
            return False
        
    def rest(self, amount=20):
        self.stamina += amount
        if self.stamina > self.maxStamina:
            self.stamina = self.maxStamina

    def gain_honour(self, amount):
        """
        Increase honour score (successful hunt, trophy, etc.).
        """
        self.honour += amount
        if self.honour > 100:
            self.honour = 100
    def lose_honour(self, amount):
        """
        Decrease honour score (cowardice, breaking code, selling fake shoes).
        """
        self.honour -= amount
        if self.honour < 0:
            self.honour = 0

    def record_kill(self):
        """Record a successful kill (for tracking)."""
        self.kills += 1
    
    def set_carrying(self, load):
     
        self.loadCarrying = load
        if load > 100:
            self.encumbered = True
            print("Your too heavy! Drop some load to continue")
            return False
    
    def get_honour_rank(self):
        
        if self.honour >= 80:
            return "Legendary"
        elif self.honour >= 60:
            return "Honoured"
        elif self.honour >= 40:
            return "Neutral"
        elif self.honour >= 20:
            return "Dishonoured"
        else:
            return "Disgraced Exiled"
        
    def get_clan_status(self, dek):
         
        if dek.honour < 20:
            return "EXILE"
        elif dek.honour < 40:
            return "DISAPPROVED"
        
        # feather has strict expectations
        if self.name == "Father":
            if dek.kills < 2:  
                return "DISAPPROVED"
            elif dek.honour >= 60 and dek.kills >= 3:
                return "ACCEPTED"
        
        
        if self.name == "Brother":
            if dek.honour > self.honour:
                return "DISAPPROVED"  #jealous
        
     
        if dek.honour >= 60:
            return "ACCEPTED"
        else:
            return "NEUTRAL"
            
    def __str__(self):
        base = super().__str__()
        return (f"{base}\n"
                f"  Stamina: {self.stamina}/{self.maxStamina} | "
                f"Honour: {self.honour} ({self.get_honour_rank()}) | "
                f"Kills: {self.kills}")
    


    def clan_dialogue(self, dek):
        """improved dialogue"""
        status = self.get_clan_status(dek)
        
        if self.name == "Father":
            messages = {
                "EXILE": "You are no son of mine. Leave or be slain where you stand!",

                "DISAPPROVED": "Prove yourself loser. You bring shame to our bloodline.",
                "NEUTRAL": f"You must show me your strength Dek. You have {dek.kills} kills and {dek.honour} honour.",
                "ACCEPTED": "You have earned respect g. The clan sees your worth."
            }
        elif self.name == "Brother":
            messages = {
                "EXILE": "LEAVE NOW! You bring great shame to us all",

                "DISAPPROVED": f"Still a little scared loser . I have {self.kills} kills to your {dek.kills}.",

                "NEUTRAL": "Perhaps you're not completely worthless bro.",

                "ACCEPTED": f"You fight well Dek. But I still have more honour ({self.honour} vs {dek.honour}) we can play some valorant later."
            }
        else:  # others
            messages = {
                "EXILE": f"{dek.name} is exiled. Do not speak to this loser man",

                "DISAPPROVED": f"The loser {dek.name} must prove himself.",

                "NEUTRAL": f"{dek.name} hunts with some skill. Hes still bronze in valorant though.",
                
                "ACCEPTED": f"{dek.name} has proven his worth to the clan."
            }
        
        return f"{self.name}: '{messages[status]}'"


    def get_thias_help(self,thia,grid):
        
        print(f"{self.name} uses Thia's scan to assess the area.")

        scan_results = thia.scan_area(grid, scan_range=5)

        if scan_results['boss']:
            boss = scan_results['boss']
            print(f"{thia.name}: 'WARNING - Ultimate Adversary detected {boss['distance']} cells away!'")
    
        if len(scan_results['monsters']) > 0:
            closest_monster = min(scan_results['monsters'], key=lambda m: m['distance'])
            print(f"{thia.name}: 'Closest threat: {closest_monster['name']} at distance {closest_monster['distance']}'")
        else:
            print(f"{thia.name}: 'Area is clear of threats.'")
        
        return scan_results
        
        # utilise thias scan to help dek find prey or avoid danger


    def carry_synthetic(self, synthetic:Synthetic):
        # help damaged synthetics
        if not synthetic.isDamaged:
            return False
        
        if self.loadCarrying > 50:
            print(f"{self.name} is too encumbered to carry {synthetic.name}.")
            return False
        
        if self.carrying_target is not None:
            print(f"{self.name} is already carrying {self.carrying_target.name}!")
            return False
        
        Grid.remove_agent(synthetic)
            
        self.loadCarrying += 50
        print(f"{self.name} is carrying {synthetic.name} for repairs.")
        return True
    
    def drop_synthetic(self):
        grid = Grid()
        if grid.is_empty(self.x,self.y):
            grid.place_agent(self.carrying_target,self.x,self.y)
            print(f"{self.name} drops {self.carrying_target.name}")

        else:
            placed = False
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx ==0 and dy ==0:
                        continue
                    drop_x = self.x + dx
                    drop_y = self.y + dy
                    if grid.is_empty(drop_x,drop_y):
                        grid.place_agent(self.carrying_target,drop_x,drop_y)
                        print(f"{self.name} drops {self.carrying_target.name} at ({drop_x},{drop_y})")
                        placed = True
                        break
                if placed:
                    break
            if not placed:
                print(f"{self.name} could not find a place to drop {self.carrying_target.name}!")
                return False


        if self.loadCarrying > 0:
            self.loadCarrying = 0
            print(f"{self.name} puts down the synthetic")
            return True
        return False

    def collect_resource(self, resource):
        """Collect a resource from the ground."""
        if resource.collected:
            return False
        
        # Check if we can carry it (only if not already encumbered)
        if self.loadCarrying > 80:
            return False
        
        resource.collected = True
        self.loadCarrying += 10  #resources add some weight
        if not hasattr(self, 'inventory'):
            self.inventory = []
        self.inventory.append(resource)
        return True
    
    def use_resource(self, resource):
        """Use a collected resource."""
        if not hasattr(self, 'inventory') or resource not in self.inventory:
            return False
        
      
        success = resource.use(self)
        
        
        if success:
            self.inventory.remove(resource)
            if self.loadCarrying > 0:
                self.loadCarrying = max(0, self.loadCarrying - 10)
        
        return success
    
    def repair_synthetic(self, synthetic):
        """Use a repair kit to repair a synthetic."""
        if not hasattr(self, 'inventory'):
            return False
        
        #find repair kit
        repair_kit = None
        for item in self.inventory:
            if hasattr(item, 'resource_type') and item.resource_type == "repair_kit":
                repair_kit = item
                break
        
        if not repair_kit:
            return False
        
        
        success = repair_kit.use(synthetic)
        
        
        if success:
            self.inventory.remove(repair_kit)
            if self.loadCarrying > 0:
                self.loadCarrying = max(0, self.loadCarrying - 10)
        
        return success


    



# Test the Predator class
if __name__ == "__main__":
    print("Testing Predator class...\n")
    

    dek = Predator(10, 10, "Dek", isDek=True)
    print("Created Dek:")
    print(dek)

    print("\n--- Testing Stamina ---")
    print(f"Using 30 stamina: {dek.useStamina(30)}")
    print(f"Stamina now: {dek.stamina}")
    
    print(f"Trying to use 80 stamina: {dek.useStamina(80)}")
    print(f"Stamina still: {dek.stamina} (insufficient, action failed)")
    
    print("Resting...")
    dek.rest()
    print(f"Stamina after rest: {dek.stamina}")

    print("\n--- Testing Honour System ---")
    print(f"Starting honour: {dek.honour} ({dek.get_honour_rank()})")
    
    dek.gain_honour(30)
    print(f"After gaining 30: {dek.honour} ({dek.get_honour_rank()})")
    
    dek.lose_honour(50)
    print(f"After losing 50: {dek.honour} ({dek.get_honour_rank()})")
    
    
    print("\n--- Testing Kill Tracking ---")
    dek.record_kill()
    dek.record_kill()
    print(f"Kills: {dek.kills}")
    
    # creaete another predator (not Dek)
    print("\n--- Creating Clan Member ---")
    father = Predator(15, 15, "Father")
    print(f"Father symbol: '{father.symbol}' (should be 'P', not 'D')")
    print(father)
    
    print("\nPredator tests complete!")
