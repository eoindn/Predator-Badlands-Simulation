import random 
import pickle

class Qlearning:
    """
    q learning is an ai reingforcement learning algorithm that will help dek to learn from its environment and make better decisions over time.
    """


    # Learning rate (alpha): Controls how much the agent will update its q values based on new experiences.
    # Higher means it leanrs faster - may be unstable
    # lower mean its slower but more stable


    # Discount factor (gamma): Determines the importance of future rewards.
    # close to 1 means it cares more for long term rewards
    # close to 0 means it cares more for immediate rewards
    # like saying 'how far ahead should i look to make my decision'

    #Epsilon (weird e symbol)
    # Used for epsilon greedy action selection
    # Probability of taking a random action isntead of the best known action
    # Helps the agent explore or exploit
    # Youd typically decay this over time

    def __init__(self, learning_rate = 0.1, discount = 0.95, eplison = 1): # these r standard values
        

        self.q_table = {} # This is like the memory -> will store what dek learns
        self.learning_rate = learning_rate
        self.discount = discount
        self.eplison = eplison


        # stores all actions dek can take
        self.actions = [
            'hunt_monster',   
            'hunt_boss',      
            'collect_resource', 
            'rest',           
            'seek_thia',      
            'avoid_danger'     
        ]



    

    def get_state(self,predator,simulation):
        """
        - this will convert the game situation into  a simple state
        
        - returns a simple tuple based on the situation

        """



        health_state = 'high' if predator.health > 65 else (
            'medium' if predator.health > 30 else 'low'
        )

        stamina_state = 'high' if predator.stamina > 65 else 'low'


        honor_state = 'high' if predator.honor > 50 else(
            'medium' if predator.honor > 20 else 'low'
        )


        # coutn nearby monsters for threat level

        nearby_monster = 0

        for monster in simulation.monsters:
            if monster.alive:
                distance = abs(monster.x - predator.x) - abs(monster.y - predator.y)
                if distance < 5:
                    nearby_monster += 1

        threat_level = 'high' if nearby_monster >= 3 else (
            'medium' if nearby_monster == 2 else 'low'
        )


        return (health_state, stamina_state,honor_state, threat_level)
    



    def choose_action(self, state):

        """
        """