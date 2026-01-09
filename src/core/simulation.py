"""
Predator: Badlands Simulation
Main simulation engine that orchestrates the multi agent system.
"""


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random

from typing import List, Dict, Optional
from core.grid import Grid
from entities.agent import Agent
from entities.predator import Predator
from entities.monster import Monster
from entities.synthetics import Synthetic
from systems.movement import MovementSystem
from entities.trap import Trap
from entities.resource import Resource
from systems.ClanCode import ClanCode
from ai.reinforcement import Qlearning
from generation.hazards import HazardGenerator
from generation.hazards import DynamicHazards

class Simulation:
    
    
    def __init__(self, width=20, height=20, num_predators=3, num_monsters=5, num_synthetics=2):
      
        self.grid = Grid(width, height)
        self.width = width
        self.height = height
        
        #track all entities
        self.predators: List[Predator] = []
        self.monsters: List[Monster] = []
        self.synthetics: List[Synthetic] = []
        self.traps: List[Trap] = []
        self.resources: List[Resource] = []
        self.all_agents: List[Agent] = []
        self.current_weather = "Clear"
        self.q_learning = Qlearning()
        
        #simulation state
        self.turn = 0
        self.max_turns = 100
        self.running = True
        
        # Stat
        self.stats = {
            'turns': 0,
            'deaths': 0,
            'kills': 0,
            'combats': 0,
            'resources_collected': 0}
        
        self.last_combat_message_turn = -1
        self.combat_message_cooldown = 3  # only print combat messages every 3 turns
        self.last_challenge_turn = {}  #track last challenge turn per predator
        self.challenge_cooldown = 10  #only challenge every 10 turns
        
        #initialise entities
        self._spawn_entities(num_predators, num_monsters, num_synthetics)
    
    def _spawn_entities(self, num_predators, num_monsters, num_synthetics):
        
        print("Spawning entities...")
        
        
        x, y = self._find_empty_position()
        dek = Predator(x, y, name="Dek", isDek=True)
       

        dek.q_learning = self.q_learning
        dek.current_state = None
        dek.last_action = None
        print(f"Dek has q learning ")

        self.grid.place_agent(dek, x, y)
        self.predators.append(dek)
        self.all_agents.append(dek)
        print(f"  Spawned Dek at ({x}, {y})")
        
      
        x, y = self._find_empty_position()
        brother = Predator(x, y, name="Brother", isDek=False)
        self.grid.place_agent(brother, x, y)
        self.predators.append(brother)
        self.all_agents.append(brother)
        print(f"  Spawned Brother at ({x}, {y})")
        
        
        x, y = self._find_empty_position()
        father = Predator(x, y, name="Father", isDek=False)
        self.grid.place_agent(father, x, y)
        self.predators.append(father)
        self.all_agents.append(father)
        print(f"  Spawned Father at ({x}, {y})")
        
       
        for i in range(max(0, num_predators - 3)):
            x, y = self._find_empty_position()
            predator = Predator(x, y, name=f"Predator{i+1}", isDek=False)
            self.grid.place_agent(predator, x, y)
            self.predators.append(predator)
            self.all_agents.append(predator)
            print(f"  Spawned Predator{i+1} at ({x}, {y})")

        
        # new spawn traps functionality
        num_traps = random.randint(3, 5)  # More traps
        for i in range(num_traps):
            x, y = self._find_empty_position()
            trap = Trap(x, y, symbol="!", name=f"Trap_{i+1}")
            #not goin to palce on the grid as its hidden
            self.traps.append(trap)  
            print(f"  Spawned {trap.name} at ({x}, {y}) [HIDDEN]")

        
    
        for i in range(num_monsters):
            x, y = self._find_empty_position()
            is_boss = (i == 0)
            name = "Ultimate Adversary" if is_boss else f"Monster{i+1}"
            monster = Monster(x, y, name=name, is_boss=is_boss)
            self.grid.place_agent(monster, x, y)
            self.monsters.append(monster)
            self.all_agents.append(monster)
            print(f"  Spawned {name} at ({x}, {y})")
        
        
        x, y = self._find_empty_position()
        thia = Synthetic(x, y, name="Thia", isThia=True)
        self.grid.place_agent(thia, x, y)
        self.synthetics.append(thia)
        self.all_agents.append(thia)
        print(f"  Spawned Thia at ({x}, {y})")
        
        # Spawn resources
        if self.turn > 10:
            num_resources = random.randint(1, 2)
        elif self.turn > 30:
            num_resources = random.randint(2, 4)
        else:
            num_resources = random.randint(4, 8)
        resource_types = ["repair_kit", "stamina_boost", "med_kit", "sword_of_despair_and_destruction"]
        for i in range(num_resources):
            x, y = self._find_empty_position()
            resource_type = random.choice(resource_types)
            resource = Resource(x, y, resource_type=resource_type)
            self.grid.place_agent(resource, x, y)
            self.resources.append(resource)
            print(f"  Spawned {resource.name} at ({x}, {y})")
        
        print(f"\nTotal entities spawned: {len(self.all_agents)}")
        
    def _find_empty_position(self):

        attempts = 0
        while attempts < 100:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.grid.is_empty(x, y):
                return x, y
            attempts += 1
        # Fallback: find first empty
        for y in range(self.height):
            for x in range(self.width):
                if self.grid.is_empty(x, y):
                    return x, y
        raise Exception("Grid is full!")
    
    def _move_agent_smart(self, agent: Agent):
        
        if not agent.alive:
            return False
        
        target = None
        
        if isinstance(agent, Predator):
            if agent.stamina < 5:
                agent.rest(10)
                print(f"{agent.name} out of stamina, resting...")
                return False
        
        if isinstance(agent, Predator):
            for monster in self.monsters:
                if monster.alive and monster.is_boss: 
                    target = (monster.x, monster.y)
                    break
        
        #onster hunt predators
        if isinstance(agent, Monster):
            closest_predator = None
            closest_dist = float('inf')
            for pred in self.predators:
                if pred.alive:  
                    dist = MovementSystem.manattan_distance((agent.x, agent.y), (pred.x, pred.y))  # Fixed typo
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_predator = pred
            if closest_predator:
                target = (closest_predator.x, closest_predator.y)
        
    
        if target:
            success = MovementSystem.move_towards_target(agent, target, self.grid)  # Fixed typo
            if success and isinstance(agent, Predator):
                stamina_cost = 5
                if hasattr(agent, 'loadCarrying') and agent.loadCarrying > 10:
                    stamina_cost = 10
                    print(f"{agent.name} is carrying a load, increased stamina cost!")
                agent.useStamina(stamina_cost)  
            return success
        
        #fa;ilback to random movement
        return self._move_agent_random(agent)
        
    def _move_agent_random(self, agent: Agent):
        """Move an agent to a random adjacent position."""
        if not agent.alive:
            return False
        
        
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = agent.x + dx
        new_y = agent.y + dy
        
        return self.grid.move_agent(agent, new_x, new_y)
    
    def _check_combat(self, agent: Agent):
        """Check if agent is adjacent to an enemy and initiate combat."""
        if not agent.alive:
            return

       
        
     
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                
                if random.random() > 0.40:
        
                    return
                
                check_x = agent.x + dx
                check_y = agent.y + dy
                target = self.grid.get_cell(check_x, check_y)
                
            
                if target is None or isinstance(target, Trap):
                    continue
                
               
                if not hasattr(target, 'alive') or not target.alive:
                    continue
                
                #see if they're enemies
                if isinstance(agent, Predator) and isinstance(target, Monster):
                    self._resolve_combat(agent, target)
                elif isinstance(agent, Monster) and isinstance(target, Predator):
                    self._resolve_combat(target, agent)
                elif isinstance(agent, Predator) and isinstance(target, Synthetic):
                    if random.random() < 0.3: 
                        self._resolve_combat(agent, target)
    
    def _resolve_combat(self, attacker: Agent, defender: Agent):


        if not attacker.alive or not defender.alive:
            return
        
        # if attacker is a Predator
        if isinstance(attacker, Predator):
            #check attack 
            if not ClanCode.should_allow_action(attacker, defender, "attack"):
                honor_change, msg = ClanCode.calculate_honor_change(attacker, defender, "attack")
                if honor_change != 0:
                    attacker.gain_honour(honor_change) if honor_change > 0 else attacker.lose_honour(abs(honor_change))
                if msg:
                    print(msg)
                return  
        
        self.stats['combats'] += 1
        
        
        if isinstance(attacker, Monster):
            damage = attacker.damage
        elif isinstance(attacker, Predator):
            base_damage = random.randint(20, 40)
            weapon_buff = getattr(attacker, 'weapon_damage_buff', 0)
            damage = base_damage + weapon_buff
        else:
            damage = random.randint(10, 20)
        
        # apply damage
        still_alive = defender.take_damage(damage)
        
        
        if isinstance(defender, Synthetic):
            defender.judge_damage()
        
        # Only print combat messages occasionally to reduce spam
        if self.turn - self.last_combat_message_turn >= self.combat_message_cooldown or not still_alive:
            print(f"  ⚔️  {attacker.name} attacks {defender.name} for {damage} damage!")
            self.last_combat_message_turn = self.turn
        
        if not still_alive:
            self.stats['deaths'] += 1
            print(f"{defender.name} has been defeated!")
            
      
            self.grid.remove_agent(defender)
            
            
            if isinstance(attacker, Predator):
                attacker.record_kill()
                
                
                honor_change, msg = ClanCode.calculate_honor_change(attacker, defender, "kill")
                if honor_change > 0:
                    attacker.gain_honour(honor_change)
                else:
                    attacker.lose_honour(abs(honor_change))
                
                if msg:
                    print(msg)
                
                self.stats['kills'] += 1
            
            # emove from lists...


            # ql earning reward for Dek
        if attacker.isDek and hasattr(attacker, 'q_learning'):
            if attacker.current_state and attacker.last_action:
                action_result = 'killed_boss' if (isinstance(defender, Monster) and defender.is_boss) else 'killed_monster'
                next_state = attacker.q_learning.get_state(attacker, self)
                reward = attacker.q_learning.get_reward(attacker, action_result)
                attacker.q_learning.update(attacker.current_state, attacker.last_action, reward, next_state)
                


    
    def _update_agents(self):
        """Update all agents (movement, combat, etc.)."""
      
        random.shuffle(self.all_agents)
        
        for agent in self.all_agents[:]:  # Copy list to avoid modification issues
            if not agent.alive:
                continue
            # Move agent
            moved = False
            # if isinstance(agent, Predator) and agent.isDek:
            #     print(f"[debug] Dek's turn hasattr q_learning: {hasattr(agent, 'q_learning')}")

            # Use Q-learning for Dek
            if isinstance(agent, Predator) and agent.isDek and hasattr(agent, 'q_learning'):
                moved = self._dek_q_learning_actions(agent)
                if moved:
                    self._check_traps(agent)
                    self._check_resources(agent)
            elif random.random() < 0.7:
                moved = self._move_agent_smart(agent)
                if moved:
                    self._check_traps(agent)
                    self._check_resources(agent)



            # Dek can pick up thia if shes damaged 
            if isinstance(agent, Predator) and agent.isDek:
                if agent.carrying_target is None:
                    for synthetic in self.synthetics:
                        if synthetic.alive and synthetic.isThia and synthetic.isDamaged:


                            #see if its close enough
                            distance = abs(agent.x - synthetic.x) + abs(agent.y - synthetic.y) 
                            if distance <= 1:
                                if agent.carry_synthetic(synthetic):
                                    print(f"  {agent.name} picked up {synthetic.name}!")
                                break
                
            
            # Check for combat
            self._check_combat(agent)
            
            # Check resources and repair Thia
            if isinstance(agent, Predator):
                self._check_resources(agent)


            # u[date for new procedural hazards
                hit, damage, hazard_type = self.hazard_generation.check_hazard_damage(agent)
                if hit:
                    agent.take_damage(damage)
                    print(f"{agent.name} hit by {hazard_type} for {damage} damage!")


            # occasionalyl challeng eto reduce spam 
            if isinstance(agent, Predator) and not agent.isDek:
                last_challenge = self.last_challenge_turn.get(agent.name, -self.challenge_cooldown)
                if self.turn - last_challenge >= self.challenge_cooldown:
                    dek = next((p for p in self.predators if p.isDek and p.alive), None)
                    if dek:
                        if agent.challenge_dek(dek, self.grid):
                            self.last_challenge_turn[agent.name] = self.turn


            
            
            if isinstance(agent, Predator):
                if agent.stamina < agent.maxStamina:
                    agent.rest(5)  # Regenerate stamina
            
            # Check if synthetics are damaged
            if isinstance(agent, Synthetic) and agent.isThia:
                agent.judge_damage()

    def _apply_weather_effects(self):
        """Apply weather effects to all agents."""
        # Update weather every 10 turns
        if self.turn % 10 == 0:
            self.current_weather = self.grid.weather_system()
            if self.turn > 0:  # Don't print on turn 0
                print(f"\n Weather changed: {self.current_weather}")
        
        # Effects everyone
        if self.current_weather == "hot":
            for pred in self.predators:
                if pred.alive:
                    pred.useStamina(2) 





        elif self.current_weather == "thunder_storm":
            # Random damage chance due to reduced visibility
            for agent in self.all_agents:
                if agent.alive and random.random() < 0.1:
                    agent.take_damage(5)



    def _check_traps(self, agent):
        """Check if agent stepped on a trap and trigger it."""
        if not agent.alive:
            return
        
      
        for trap in self.traps[:]: 
            if trap.x == agent.x and trap.y == agent.y and not trap.is_triggered:
                print(f"{agent.name} stepped on {trap.name}!")
                
                damage = trap.damage()
                still_alive = agent.take_damage(damage)
                trap.is_triggered = True
                print(f"Trap deals {damage} damage! {agent.name} HP: {agent.health}/{agent.max_health}")
                # preds loose honor for triggering traps
                if isinstance(agent, Predator):
                    agent.lose_honour(5)
                    print(f"{agent.name} loses 5 honour for carelessness!")
                if not still_alive:
                    print(f" {agent.name} was killed by the trap!")
                    self._remove_dead_agent(agent)
                
                break  

    def weather_update(self):
        if self.turn % 10 == 0:
            self.current_weather = self.grid.weather_system()
            print(f"Weather changed: {self.current_weather}")

        for agent in self.all_agents:
            if not agent.alive:
                continue
            if isinstance(agent, Predator):
                if self.current_weather == "hot":
                    agent.useStamina(2)
                    if agent.stamina < 20:
                        print(f"{agent.name} is struggling in the heat, stamina reduced to {agent.stamina}. They must rest")
                        agent.rest(10)
                if self.current_weather == "cold":
                    agent.useStamina(1) #need to update this

                elif self.current_weather == "thunder_storm":
                #STRIKE BY LIGHTNING
                    if random.random() < 0.15: 
                        damage = random.randint(5, 10)
                        agent.take_damage(damage)
                        print(f" {agent.name} was struck by lightning for {damage} damage!")   


    def _remove_dead_agent(self, agent):
        #helper method to remove dead agents from simulation
        self.grid.remove_agent(agent)
        
        if isinstance(agent, Predator) and agent in self.predators:
            self.predators.remove(agent)
        elif isinstance(agent, Monster) and agent in self.monsters:
            self.monsters.remove(agent)
        elif isinstance(agent, Synthetic) and agent in self.synthetics:
            self.synthetics.remove(agent)


    def _check_resources(self, agent):
        """check if an agent's position is on a resource and collects it."""
        if not isinstance(agent, Predator):
            return False
        


     
                
    
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = agent.x + dx
                check_y = agent.y + dy
                resource_cell = self.grid.get_cell(check_x, check_y)

         
                if resource_cell is None:
                    continue
                
               
                if isinstance(resource_cell, Resource) and not resource_cell.collected:
                    if agent.collect_resource(resource_cell):
                        self.grid.remove_agent(resource_cell)
                        if resource_cell in self.resources:
                            self.resources.remove(resource_cell)
                        self.stats['resources_collected'] += 1
                        print(f"  📦 {agent.name} collected {resource_cell.name}!")
                        
                       
                        if resource_cell.resource_type == "sword_of_despair_and_destruction":
                            #equip weapon immediately
                            resource_cell.use(agent)
                        elif resource_cell.resource_type == "med_kit":
                        
                            if agent.health < agent.max_health:
                                resource_cell.use(agent)
                                if hasattr(agent, 'inventory') and resource_cell in agent.inventory:
                                    agent.inventory.remove(resource_cell)
                                    agent.loadCarrying = max(0, agent.loadCarrying - 10)
                        elif resource_cell.resource_type == "stamina_boost":
                            #us estamina boost if not full
                            if agent.stamina < agent.maxStamina:
                                resource_cell.use(agent)
                               
                                if hasattr(agent, 'inventory') and resource_cell in agent.inventory:
                                    agent.inventory.remove(resource_cell)
                                    agent.loadCarrying = max(0, agent.loadCarrying - 10)
                       
                        
                        return True
        
        
        if hasattr(agent, 'inventory') and agent.inventory:
            for synthetic in self.synthetics:
                if synthetic.isThia and synthetic.isDamaged:
                
                    dist = abs(agent.x - synthetic.x) + abs(agent.y - synthetic.y)
                    if dist <= 1:
                        if agent.repair_synthetic(synthetic):
                            # Message is printed by Resource.use()
                            return True
            
            #auro use med kits and stamina boost
            for item in agent.inventory[:]:  #copt list ot avoid modification
                if item.resource_type == "med_kit" and agent.health < 50:
                    if agent.use_resource(item):
                        
                        return True
                elif item.resource_type == "stamina_boost" and agent.stamina < 30:
                    if agent.use_resource(item):
                        return True
        
        return False

    def _dek_q_learning_actions(self, dek):
        """Use Q-Learning to decide and execute Dek's action."""
        if not hasattr(dek, 'q_learning'):
            return False
            
        current_state = dek.q_learning.get_state(dek, self)
        action = dek.q_learning.choose_action(current_state)
        
        if self.turn % 5 == 0:
            print(f"Dek Q-Learning: chose '{action}' in state {current_state}")

        action_result = 'moved'

    
        if action == "hunt_boss":
            closest_monster = None
            closest_dist = float('inf')
            for monster in self.monsters:  
                if monster.is_boss and monster.alive: 
                    dist = abs(monster.x - dek.x) + abs(monster.y - dek.y)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_monster = monster
            
            if closest_monster:
                target = (closest_monster.x, closest_monster.y)
                if MovementSystem.move_towards_target(dek, target, self.grid):
                    dek.useStamina(5)
                    action_result = 'moved'
        
        elif action == "hunt_monster":
            closest_monster = None
            closest_dist = float('inf')
            for monster in self.monsters:
                if not monster.is_boss and monster.alive:
                    dist = abs(monster.x - dek.x) + abs(monster.y - dek.y)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_monster = monster
            
            if closest_monster:
                target = (closest_monster.x, closest_monster.y)
                if MovementSystem.move_towards_target(dek, target, self.grid):
                    dek.useStamina(5)
                    action_result = 'moved'
        
        elif action == 'rest':
            if dek.stamina < dek.maxStamina:
                dek.rest(20)
                action_result = 'healed'
            else:
                action_result = 'wasted_action'
        
        elif action == 'collect_resource':
            closest_resource = None
            closest_dist = float('inf')
            for resource in self.resources:
                if not resource.collected:
                    dist = abs(resource.x - dek.x) + abs(resource.y - dek.y)
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_resource = resource
            
            if closest_resource:
                target = (closest_resource.x, closest_resource.y)
                if MovementSystem.move_towards_target(dek, target, self.grid):
                    dek.useStamina(3)
                    action_result = 'moved'
        
        elif action == 'seek_thia':
            thia = next((s for s in self.synthetics if s.isThia and s.alive), None)
            if thia:
                target = (thia.x, thia.y)
                if MovementSystem.move_towards_target(dek, target, self.grid):
                    dek.useStamina(5)
                    action_result = 'moved'
        
        elif action == 'avoid_danger':
            best_dx, best_dy = 0, 0
            best_score = -999
            
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    
                    test_x = dek.x + dx
                    test_y = dek.y + dy
                    
                    monster_count = 0
                    for monster in self.monsters:
                        if monster.alive:
                            dist = abs(monster.x - test_x) + abs(monster.y - test_y)
                            if dist < 3:
                                monster_count += 1
                    
                    score = -monster_count
                    if score > best_score:
                        best_score = score
                        best_dx, best_dy = dx, dy
            
            new_x = dek.x + best_dx
            new_y = dek.y + best_dy
            if self.grid.move_agent(dek, new_x, new_y):
                dek.useStamina(3)
                action_result = 'moved'
        
        # Update Q-table
        next_state = dek.q_learning.get_state(dek, self)
        reward = dek.q_learning.get_reward(dek, action_result)
        dek.q_learning.update(current_state, action, reward, next_state)
        
        dek.current_state = next_state
        dek.last_action = action
        
        return True



        


    
    def _check_win_conditions(self):
        """Check if simulation should end."""

        alive_monsters = [m for m in self.monsters if m.alive]
        if len(alive_monsters) == 0:
            print("\n🎉 All monsters defeated! Predators win!")
            return True
        
        # seen if all predators are dead
        alive_predators = [p for p in self.predators if p.alive]
        if len(alive_predators) == 0:
            print("\nAll predators defeated! Monsters win!")
            return True
        
        return False
    
    def run(self, display_every=5, max_turns=100):
       
        print("\n" + "="*20)
        print("PREDATOR: BADLANDS SIMULATION")
        print("="*20)
        print(f"Grid: {self.width}x{self.height}")
        print(f"Max turns: {max_turns}")
        print("="*20 + "\n")
        
        self.max_turns = max_turns
        if display_every > 0:
            print(f"\n--- Turn 0 (Initial State) ---")
            self.grid.display()
            self._print_stats()
        
        #main simulation loop
        for turn in range(1, max_turns + 1):
            self.turn = turn
            self.stats['turns'] = turn
            
        
            self._update_agents()
            self.hazard_generation.update(turn)


            self.weather_update()
            
            #periodically display
            if display_every > 0 and turn % display_every == 0:
                print(f"\n--- Turn {turn} ---")
                self.grid.display()
                self._print_stats()
            
            #check win conditions
            if self._check_win_conditions():
                break
            
            #check if simulation should continue
            if len(self.predators) == 0 or len(self.monsters) == 0:
                break


            
        
        #final display
        print(f"\n--- Final State (Turn {self.turn}) ---")
        self.grid.display()
        self._print_final_stats()

   

        dek = next((p for p in self.predators if p.isDek), None)
        if dek and hasattr(dek, 'q_learning'):
            print(f"QLEARNING STATS:")
            print(f"table size: {len(dek.q_learning.q_table)} states learned")
            print(f" Epsilon: {dek.q_learning.epsilon}")
            if len(dek.q_learning.q_table) > 0:
                print(f"   Sample states explored:")
                for i, (state, actions) in enumerate(list(dek.q_learning.q_table.items())[:3]):
                    best_action = max(actions, key=actions.get)
                    best_value = actions[best_action]
                    print(f"     State {state}: Best action = {best_action} (Q={best_value:.2f})")
        
    def _print_stats(self):
        """Print current simulation statistics."""
        alive_predators = len([p for p in self.predators if p.alive])
        alive_monsters = len([m for m in self.monsters if m.alive])
        alive_synthetics = len([s for s in self.synthetics if s.alive])
        
        print(f"\nStatistics:")
        print(f"  Turn: {self.turn}, Weather is {self.current_weather}")
        print(f"  Alive - Predators: {alive_predators}, Monsters: {alive_monsters}, Synthetics: {alive_synthetics}")
        print(f"  Combats: {self.stats['combats']}, Kills: {self.stats['kills']}, Deaths: {self.stats['deaths']}")
        print(f"  Resources collected: {self.stats['resources_collected']}, Remaining: {len(self.resources)}")
        print(f"  Traps: {len([t for t in self.traps if not t.is_triggered])}  /  {len(self.traps)} active")
        
        # Show predator honor
        if self.predators:
            print(f"\n  Predator Status:")
            for pred in self.predators:
                if pred.alive:
                    print(f"    {pred.name}: HP {pred.health}/{pred.max_health} , Stamina: {pred.stamina} "
                          f"Honor {pred.honour} ({pred.get_honour_rank()}), Kills: {pred.kills}")
    
    def _print_final_stats(self):
        """Print final simulation statistics."""
        print("\n" + "="*50)
        print("FINAL STATISTICS")
        self._print_stats()
        
    
    def test_scan(self):
        """Test the scanning functionality of synthetics."""
        print("\n--- Testing Scan Functionality ---")
        for synthetic in self.synthetics:
            if synthetic.alive and synthetic.isThia:
                print(f"\n{synthetic.name} scanning area...")
                results = synthetic.scan_area(self.grid, scan_range=3)
                
                print(f"  Monsters detected: {len(results['monsters'])}")
                for m in results['monsters']:
                    print(f"    - {m['name']} at {m['position']} (distance: {m['distance']})")
                
                print(f"  Predators detected: {len(results['predators'])}")
                for p in results['predators']:
                    print(f"    - {p['name']} at {p['position']} (distance: {p['distance']})")
                
                if results['boss']:
                    print(f"BOSS SEEN: {results['boss']['name']} at {results['boss']['position']}!")
                
                break


def main():
    
    # Create
    sim = Simulation(
        width=20,
        height=20,
        num_predators=3,
        num_monsters=5,
        num_synthetics=2
    )
    #test scan functionalitysim.test_scan()
    
    #run simulation
    sim.run(display_every=10, max_turns=50)

    
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()