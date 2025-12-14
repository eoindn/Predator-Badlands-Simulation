from entities.agent import Agent

class Resource(Agent):
    """Collectible resources on the map."""
    
    TYPES = {
        'sword_of_despair_and_destruction': {'symbol': 'W', 'damage_boost': 20},
        'repair_kit': {'symbol': 'R', 'heal_amount': 30},
        'med_kit': {'symbol': 'H', 'heal_amount': 50},
        'stamina_boost': {'symbol': 'S', 'stamina_amount': 30}
    }
    
    def __init__(self, x, y, resource_type='repair_kit'):
        if resource_type not in self.TYPES:
            raise ValueError(f"Invalid resource_type: {resource_type}. Must be one of {list(self.TYPES.keys())}")
        
        self.resource_type = resource_type
        config = self.TYPES[resource_type]
        super().__init__(x, y, config['symbol'], f"{resource_type.replace('_', ' ').title()}")
        
        # Resource properties
        self.damage_boost = config.get('damage_boost', 0)
        self.heal_amount = config.get('heal_amount', 0)
        self.stamina_amount = config.get('stamina_amount', 0)
        self.collected = False
    
    def use(self, agent):
        """Apply resource effect to agent."""
        from entities.predator import Predator
        from entities.synthetics import Synthetic
        
        if self.resource_type == 'sword_of_despair_and_destruction':
            if isinstance(agent, Predator):
                agent.weapon_damage_buff = self.damage_boost
                print(f"⚔️  {agent.name} equipped THE SWORD OF DESPAIR AND DESTRUCTION! +{self.damage_boost} damage")
                return True
        
        elif self.resource_type == 'repair_kit':
            if isinstance(agent, Synthetic):
                agent.heal(self.heal_amount)
                agent.isDamaged = False
                print(f"🔧 {agent.name} repaired for {self.heal_amount} HP")
                return True
        
        elif self.resource_type == 'med_kit':
            agent.heal(self.heal_amount)
            print(f"💉 {agent.name} healed for {self.heal_amount} HP")
            return True
        
        elif self.resource_type == 'stamina_boost':
            if isinstance(agent, Predator):
                agent.stamina += self.stamina_amount
                if agent.stamina > agent.maxStamina:
                    agent.stamina = agent.maxStamina
                print(f"⚡ {agent.name} restored {self.stamina_amount} stamina")
                return True
        
        return False
