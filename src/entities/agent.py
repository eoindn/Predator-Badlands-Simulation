class Agent:

    def __init__(self,x,y,symbol,name = "Agent"):

        self.x = y
        self.y = y

        self.symbol = symbol
        self.name = name

        self.health = 100
        self.max_health = 100
        self.alive = True
        self.stamina = 100
        self.maxStamina = 100
        self.honor = 50 #honor starts neutral

    
    

    
    def takeDamage(self,ammount):
        
        self.health -= 1

        if self.health <= 0:
            self.health = 0
            self.alive = False
            return False
        return True
    

    def heal(self,ammount):
        self.health += ammount
    def bigHeal(self):
        self.health = self.max_health

    def isAlive(self):
        return self.isAlive
    
    def getPos(self):
        return (self.x,self.y)
    
    def __str__(self):
        """String representation for debugging."""
        status = "ALIVE" if self.alive else "DEAD"
        return f"{self.name} ({self.symbol}) at ({self.x}, {self.y}) - HP: {self.health}/{self.max_health} [{status}]"
    
    def __repr__(self):
        """dev representation."""
        return f"Agent('{self.name}', pos=({self.x},{self.y}), hp={self.health})"
    

   
    

if __name__ == "__main__":
    print("Testing Agent class...\n")
    
 
    agent = Agent(5, 10, 'A', "TestAgent")
    print(f"Created: {agent}")
    
   
    print("\nTaking 30 damage")
    agent.takeDamage(30)
    print(f"After damage: {agent}")
    
    
    print("\nHealing 20")
    agent.heal(20)
    print(f"After healing: {agent}")
    

    print("\nTaking 100 damage")
    still_alive = agent.takeDamage(100)
    print(f"Still alive? {still_alive}")
    print(f"Final state: {agent}")
    
    
    print("\nCreating new agent and over-healing")
    agent2 = Agent(0, 0, 'B', "Agent2")
    agent2.heal(200)
    print(f"After healing 200: {agent2}")
    print(f"Health capped at max: {agent2.health == agent2.max_health}")
    
    print("\nAgent tests complete!")
        
        