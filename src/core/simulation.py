"""
Predator: Badlands Simulation
Main simulation engine that orchestrates the multi-agent system.
"""


import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random

from typing import List, Dict, Optional
from grid import Grid
from entities.agent import Agent
from entities.predator import Predator
from entities.monster import Monster
from entities.synthetics import Synthetic
from systems.movement import MovementSystem
from entities.trap import Trap
from systems.ClanCode import ClanCode


class Simulation:
    
    
    def __init__(self, width=20, height=20, num_predators=3, num_monsters=5, num_synthetics=2):
      
        self.grid = Grid(width, height)
        self.width = width
        self.height = height
        
        # Track all entities
        self.predators: List[Predator] = []
        self.monsters: List[Monster] = []
        self.synthetics: List[Synthetic] = []
        self.traps: List[Trap] = []
        self.all_agents: List[Agent] = []
        self.current_weather = "Clear"
        
        # Simulation state
        self.turn = 0
        self.max_turns = 100
        self.running = True
        
        # Statistics
        self.stats = {
            'turns': 0,
            'deaths': 0,
            'kills': 0,
            'combats': 0
        }
        
        # Initialise entities
        self._spawn_entities(num_predators, num_monsters, num_synthetics)
    
    def _spawn_entities(self, num_predators, num_monsters, num_synthetics):
        
        print("Spawning entities...")
        
        
        x, y = self._find_empty_position()
        dek = Predator(x, y, name="Dek", isDek=True)
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
        
        if success and isinstance(agent, Predator):
            stamina_cost = 5
            if agent.loadCarrying > 10:
                stamina_cost = 10
                print(f"{agent.name} is carrying a load, increased stamina cost!")
            
        
        
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
                agent.useStamina(5)  
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
                
                if target is None or not target.alive:
                    continue
                
                #see if they're enemies
                if isinstance(agent, Predator) and isinstance(target, Monster):
                    self._resolve_combat(agent, target)
                elif isinstance(agent, Monster) and isinstance(target, Predator):
                    self._resolve_combat(target, agent)
                elif isinstance(agent, Predator) and isinstance(target, Synthetic):
                    if random.random() < 0.3:  # 30% chance
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
            damage = random.randint(20, 40)
            boost_damage = damage + attacker.weapon_damage_buff
        else:
            damage = random.randint(10, 20)
        
        # apply damage
        still_alive = defender.take_damage(damage)
        print(f"  ⚔️  {attacker.name} attacks {defender.name} for {damage} damage!")
        
        if not still_alive:
            self.stats['deaths'] += 1
            print(f"  💀 {defender.name} has been defeated!")
            
      
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
            


    
    def _update_agents(self):
        """Update all agents (movement, combat, etc.)."""
        # Shuffle to randomize turn order
        random.shuffle(self.all_agents)
        
        for agent in self.all_agents[:]:  # Copy list to avoid modification issues
            if not agent.alive:
                continue
            
            # Move agent
            if random.random() < 0.7: 
                moved = self._move_agent_smart(agent)
                if moved:  
                    self._check_traps(agent)


            # Dek can pick up thia if shes fdamged 
            if isinstance(agent, Predator) and agent.isDek:
                if agent.carry_synthetic is None:
                    for syntehtic in self.synthetics and syntehtic.is_alive:
                        if syntehtic.isThia and syntehtic.isDamaged:

                            #check is its close enough
                            distance = abs(agent.x - syntehtic.x) + abs(agent.y - syntehtic.y) 
                            if distance <= 1:
                                agent.pick_up_synthetic(syntehtic)
                                print(f" {agent.name} picked up {syntehtic.name}!")
                                break
                
            
            # Check for combat
            self._check_combat(agent)


            if isinstance(agent,Predator) and not agent.isDek:
                dek = next((p for p in self.predators if p.isDek and p.alive), None)
                if dek:
                    agent.challenge_dek(dek, self.grid)


            
            # Update stamina for predators
            if isinstance(agent, Predator):
                if agent.stamina < agent.maxStamina:
                    agent.rest(5)  # Regenerate stamina


        def _apply_weather_effects(self):
            
            #pdate weather every 10 turns
            if self.turn % 10 == 0:
                self.current_weather = self.grid.weather_system()
                print(f"\n Weather changed: {self.current_weather}")
            
            #effects everyone
            if self.current_weather == "hot":
                for pred in self.predators:
                    if pred.alive:
                        pred.useStamina(2) 
            elif self.current_weather == "thunder_storm":
                # eandom damage chance due to reduced visibility
                for agent in self.all_agents:
                    if agent.alive and random.random() < 0.1:
                        agent.take_damage(5)

        if moved:
            self._check_resources(agent)
            self._check_traps(agent)



    def _check_traps(self, agent):
        """Check if agent stepped on a trap and trigger it."""
        if not agent.alive:
            return
        
      
        for trap in self.traps[:]: 
            if trap.x == agent.x and trap.y == agent.y and not trap.is_triggered:
                print(f"  💥 {agent.name} stepped on {trap.name}!")
                
                damage = trap.damage()
                still_alive = agent.take_damage(damage)
                trap.is_triggered = True




                
                print(f"     Trap deals {damage} damage! {agent.name} HP: {agent.health}/{agent.max_health}")
                
                # preds loose honor for triggering traps
                if isinstance(agent, Predator):
                    agent.lose_honour(5)
                    print(f"     {agent.name} loses 5 honour for carelessness!")
                
                if not still_alive:
                    print(f"  ☠️  {agent.name} was killed by the trap!")
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
                    agent.useStamina(1) # need to update this

                elif self.current_weather == "thunder_storm":
                #STRIKE BY LIGHTNING
                    if random.random() < 0.15: 
                        damage = random.randint(5, 10)
                        agent.take_damage(damage)
                        print(f" {agent.name} was struck by lightning for {damage} damage!")   


    def _remove_dead_agent(self, agent):
        # helper method to remove dead agents from simulation
        self.grid.remove_agent(agent)
        
        if isinstance(agent, Predator) and agent in self.predators:
            self.predators.remove(agent)
        elif isinstance(agent, Monster) and agent in self.monsters:
            self.monsters.remove(agent)
        elif isinstance(agent, Synthetic) and agent in self.synthetics:
            self.synthetics.remove(agent)


    def _check_resources(self,agent):

        # chekcs if an agents position is on a resource and colelcts it

        if not isinstance(agent, Predator):
            return False
        
        for dx in [-1, 0, 1]:
            for dy in [-1,0,1]:
                check_x = agent.x + dx
                check_y = agent.y + dy
                resource_cell = self.grid.get_cell(check_x, check_y)


                if isinstance(cell, Resource) and not cell.collected:
                    if agent.collect_resource(cell):
                        self.grid.remove_agent(cell)

                    return
                
        


    
    def _check_win_conditions(self):
        """Check if simulation should end."""
        # Check if all monsters are dead
        alive_monsters = [m for m in self.monsters if m.alive]
        if len(alive_monsters) == 0:
            print("\n🎉 All monsters defeated! Predators win!")
            return True
        
        # Check if all predators are dead
        alive_predators = [p for p in self.predators if p.alive]
        if len(alive_predators) == 0:
            print("\n💀 All predators defeated! Monsters win!")
            return True
        
        return False
    
    def run(self, display_every=5, max_turns=100):
       
        print("\n" + "="*50)
        print("PREDATOR: BADLANDS SIMULATION")
        print("="*50)
        print(f"Grid: {self.width}x{self.height}")
        print(f"Max turns: {max_turns}")
        print("="*50 + "\n")
        
        self.max_turns = max_turns
        
        # Initial display
        if display_every > 0:
            print(f"\n--- Turn 0 (Initial State) ---")
            self.grid.display()
            self._print_stats()
        
        # Main simulation loop
        for turn in range(1, max_turns + 1):
            self.turn = turn
            self.stats['turns'] = turn
            
            # Update all agents
            self._update_agents()


            self.weather_update()
            
            # Display periodically
            if display_every > 0 and turn % display_every == 0:
                print(f"\n--- Turn {turn} ---")
                self.grid.display()
                self._print_stats()
            
            # Check win conditions
            if self._check_win_conditions():
                break
            
            # Check if simulation should continue
            if len(self.predators) == 0 or len(self.monsters) == 0:
                break
        
        # Final display
        print(f"\n--- Final State (Turn {self.turn}) ---")
        self.grid.display()
        self._print_final_stats()
    
    def _print_stats(self):
        """Print current simulation statistics."""
        alive_predators = len([p for p in self.predators if p.alive])
        alive_monsters = len([m for m in self.monsters if m.alive])
        alive_synthetics = len([s for s in self.synthetics if s.alive])
        
        print(f"\n📊 Statistics:")
        print(f"  Turn: {self.turn}, Weather is {self.current_weather}")
        print(f"  Alive - Predators: {alive_predators}, Monsters: {alive_monsters}, Synthetics: {alive_synthetics}")
        print(f"  Combats: {self.stats['combats']}, Kills: {self.stats['kills']}, Deaths: {self.stats['deaths']}")
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
        print("="*50)
        self._print_stats()
        print("="*50)
    
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
                    print(f"  ⚠️  BOSS DETECTED: {results['boss']['name']} at {results['boss']['position']}!")
                
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
    
    #run simulatio
    sim.run(display_every=10, max_turns=50)
    
    print("\nSimulation complete!")


if __name__ == "__main__":
    main()