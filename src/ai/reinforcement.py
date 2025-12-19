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
        decides what action to take

        - sometimes explores and tries random things
        - sometimes exploits and uses what it knows to make the best choice

        """

        # checks ifstate is in memory
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}


        # Exploration : tries soemthing random 20 perecetn of the time
        if random.random() < self.eplison:
            action = random.choice(self.actions)
            return action
        


        best_action = max(self.q_table[state], key=self.q_table[state].get)

        return best_action
    


    def update(self, state, action, reward, next_state):
        """
        Core learning process for Q-learning

        Q(state, action) = old value + learning rate * (reward + discount * best_future - old value)

        """


        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.actions}

        if next_state not in self.q_table:
            self.q_table[next_state] = {action: 0.0 for action in self.actions}

        # check what we think this action was worth
        current_q = self.q_table[state][action]

        max_next_q = max(self.q_table[next_state].values())

        # update knowledge
        # reward is the immediate payoff dek got
        # max_next_q = best possible future play off

        new_q = current_q + self.learning_rate * (reward + self.discount * max_next_q - current_q)



    def get_reward(self, predator, action_result):
        """
        Score an outcome which says: did this action work out well?
        
        Positive rewards = good outcomes
        Negative rewards = bad outcomes
        """
        # huge w
        if action_result == 'killed_boss':
            return 100  # Huge reward!
        elif action_result == 'killed_monster':
            return 20
        elif action_result == 'gained_honour':
            return 10
        elif action_result == 'collected_resource':
            return 5
        elif action_result == 'healed':
            return 3
        
        # mid w
        elif action_result == 'moved':
            return 0
        
        # l's
        elif action_result == 'took_damage':
            return -10
        elif action_result == 'lost_honour':
            return -15
        elif action_result == 'died':
            return -100  # cooked
        elif action_result == 'wasted_action':
            return -2
        
        return 0  
    



    def save(self, filename='q_table.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)
        print(f"Saved Q table with {len(self.q_table)} states")
    
    def load(self, filename='q_table.pkl'):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
            print(f"Loaded Q table with {len(self.q_table)} states")
            return True
        except FileNotFoundError:
            print("No saved Q table found , starting fresh")
            return False
        


