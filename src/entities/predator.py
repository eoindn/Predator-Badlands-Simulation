from entities.agent import Agent

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

        #whats he doing and whats he done >:)
        self.kills = 0 
        self.loadCarrying = 0
        self.encumbered = False
    

    def challenge_dek(self, dek, grid):
        dek_position = abs(self.x - dek.x) + abs(self.y - dek.y)

        if dek_position < 2:
            return False

        if self.name == "Father":
            if self.honor < 40:
                print(f" {self.name}: You disohonor the clan {dek.name}! Prove yourself worthy")
                self.dek_relationship -= 5
                return True
        
        elif self.name == "Brother":
            if dek.kills > self.kills + 2:
                print(f"\n  {self.name}: 'Your success makes you arrogant, Dek!'")
                self.dek_relationship -= 5
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
        
    def __str__(self):
        """Detailed string representation."""
        base = super().__str__()
        return (f"{base}\n"
                f"  Stamina: {self.stamina}/{self.maxStamina} | "
                f"Honour: {self.honour} ({self.get_honour_rank()}) | "
                f"Kills: {self.kills}")
    


    def clan_dialogue(self, dek):
    #s imple dialogue based on honour for noe
        status = self.get_clan_status(dek)
        
        if self.clan_role == "father":
            messages = {
                "EXILE": "You are no son of mine leave or be slain where you stand!",
                "DISAPPROVED": "Prove yourself you loser runt.",
                "NEUTRAL": "Show me your strength pad thai.",
                "ACCEPTED": "You have earned respect young warrior."
            }
        else:  # brother or other pred
            messages = {
                "EXILE": "LEAVE NOW! You bring shame to us all!",
                "DISAPPROVED": "Still a dumb loser , I see.",
                "NEUTRAL": "Perhaps you're not a dumb loser.",
                "ACCEPTED": "You fight well brah."
            }
        
        return f"{self.name}: {messages[status]}"
    

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
