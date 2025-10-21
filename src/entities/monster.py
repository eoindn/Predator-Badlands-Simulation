from entities.agent import Agent

class Monster(Agent):

    def __init__(self,x,y,name="Monster",is_boss = False):
        symbol = 'X' if is_boss else 'M'

        super().__init__(x,y,symbol,name)

        self.is_boss = is_boss
        self.damage = 30 if is_boss else 10


        if is_boss:
            self.health = 350
            self.max_health = 350

    def attack_damage(self):
        return self.attack_damage
    
    def threat_level(self):
        if self.is_boss:
            return "Ultimate Adversary! Fight or been slaughtered where you stand!"
        else:
            return "Monster Encountered!"



def __str__(self):
        
        base = super().__str__()
        return f"{base}\n  Threat: {self.get_threat_level()} | Damage: {self.damage}"



if __name__ == "__main__":
    print("Testing Monster class...\n")
    
    # Create regular monster
    monster = Monster(5, 5, "Cave Creature")
    print("Regular Monster:")
    print(monster)
    print()
    
    # Create boss
    boss = Monster(15, 15, "Ultimate Adversary", is_boss=True)
    print("Boss Monster:")
    print(boss)
    print()
    
  
    print("--- Testing Combat ---")
    print(f"Regular monster damage: {monster.attack_damage()}")
    print(f"Boss damage: {boss.attack_damage()}")
    
    
    print("\nBoss takes 50 damage...")
    boss.take_damage(50)
    print(f"Boss health: {boss.health}/{boss.max_health}")
    
    print("\nMonster tests complete!")
        