class Agent:

    def __init__(self,x,y,symbol,name = "Agent"):

        self.x = x
        self.y = y

        self.symbol = symbol
        self.name = name

        self.health = 100
        self.max_health = 100
        self.alive = True
        self.stamina = 100
        self.max_stamina = 100
        self.honor = 50 #honor starts neutral

    
    

    
    def take_damage(self,ammount):
        
        self.health -= ammount

        if self.health <= 0:
            self.health = 0
            self.alive = False
            return False
        return True
    

    def heal(self,ammount):
        self.health += ammount
        if self.health > self.max_health:
            self.health = self.max_health
    def big_heal(self):
        self.health = self.max_health

    def is_alive(self):
        return self.alive
    
    def get_pos(self):
        return (self.x,self.y)
    
    
    
    
    

   
    

if __name__ == "__main__":
    print("Testing Agent class...\n")
    
 
    agent = Agent(5, 10, 'A', "TestAgent")
    print(f"Created: {agent}")
    
   
    print("\nTaking 30 damage")
    agent.take_damage(30)
    print(f"After damage: {agent}")
    
    
    print("\nHealing 20")
    agent.heal(20)
    print(f"After healing: {agent}")
    

    print("\nTaking 100 damage")
    still_alive = agent.take_damage(100)
    print(f"Still alive? {still_alive}")
    print(f"Final state: {agent}")
    
    
    print("\nCreating new agent and over-healing")
    agent2 = Agent(0, 0, 'B', "Agent2")
    agent2.heal(200)
    print(f"After healing 200: {agent2}")
    print(f"Health capped at max: {agent2.health == agent2.max_health}")
    
    print("\nAgent tests complete!")
        
        