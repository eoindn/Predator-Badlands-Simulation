"""
Predator: Badlands Simulation
Main simulation engine that orchestrates the multi-agent system.
"""

import random
import sys
import os
from typing import List, Dict, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import core components
from core.grid import Grid

# Import entities
from entities.agent import Agent
from entities.predator import Predator
from entities.monster import Monster
from entities.synthetics import Synthetic

# Import systems
from systems.movement import MovementSystem


class Simulation:
    """
    This simulation class that manages the game world and entities so i can test the game and its functionality.
    
   
    """
    
    def __init__(self, width=20, height=20, num_predators=3, num_monsters=5, num_synthetics=2):
        """
        
        
        Args:
            width: Grid width (default 20)
            height: Grid height (default 20)
            num_predators: Number of Predator agents to spawn
            num_monsters: Number of Monster agents to spawn
            num_synthetics: Number of Synthetic agents to spawn
        """
        self.grid = Grid(width, height)
        self.width = width
        self.height = height
        
        # Track all entities
        self.predators: List[Predator] = []
        self.monsters: List[Monster] = []
        self.synthetics: List[Synthetic] = []
        self.all_agents: List[Agent] = []
        
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
        """Spawn all entities at random positions."""
        print("Spawning entities...")
        
        # gonna spawndek first
        x,y = self._find_empty_position()
        Dek = Predator(x,y,name="Dek",isDek = True)
        self.grid.place_agent(Dek,x,y)
        self.predators.append(Dek)
        self.all_agents.append(Dek)
        print(f"Dek spawned at ({x} {y})")

        #the dad
        x,y = self._find_empty_position()
        father = Predator(x,y ,name = "Father",isDek = False)
        self.grid.place_agent(father,x,y)
        self.predators.append(father)
        self.all_agents.append(father)
        print(f"Father spawend at ({x} {y})")

        # the brother
        x, y = self._find_empty_position()  # NEW position!
        brother = Predator(x, y, name="Brother", isDek=False)
        self.grid.place_agent(brother, x, y)
        self.predators.append(brother)
        self.all_agents.append(brother)
        print(f"  Spawned Brother at ({x}, {y})")


        for i in range(3, num_predators):
            x,y = self._find_empty_position()
                
            predator = Predator(x, y, name=f"Predator{i+1}", isDek=False)
            self.grid.place_agent(predator,x,y)
            self.agents.append(predator)
            self.all_agents.append(predator)
            print(f"Spawned {predator.nane} at ({x} {y})")
            

        
        #pawn Monster(one boss)
        for i in range(num_monsters):
            x, y = self._find_empty_position()
            is_boss = (i == 0)  # First monster is boss
            name = "Ultimate Adversary" if is_boss else f"Monster{i+1}"
            monster = Monster(x, y, name=name, is_boss=is_boss)
            self.grid.place_agent(monster, x, y)
            self.monsters.append(monster)
            self.all_agents.append(monster)
            print(f"  Spawned {name} at ({x}, {y})")
        
        #Spawn Synthetic (Thia)
        for i in range(num_synthetics):
            x, y = self._find_empty_position()
            is_thia = (i == 0)  # First synthetic is Thia
            name = "Thia" if is_thia else f"Synthetic{i+1}"
            synthetic = Synthetic(x, y, name=name, isThia=is_thia)
            self.grid.place_agent(synthetic, x, y)
            self.synthetics.append(synthetic)
            self.all_agents.append(synthetic)
            print(f"  Spawned {name} at ({x}, {y})")
        
        print(f"\nTotal entities spawned: {len(self.all_agents)}")
    
    def _find_empty_position(self):
        """Find a random empty position on the grid."""
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
        """Move an agent intelligently toward a target, or randomly if no target."""
        if not agent.alive:
            return False
        
        target = None
        
        if isinstance(agent, Predator):
            if agent.stamina < 5:
                agent.rest(10)
                print(f"{agent.name} out of stamina, resting...")
                return False
        
        # Predators hunt boss monsters
        if isinstance(agent, Predator):
            for monster in self.monsters:
                if monster.alive and monster.is_boss:  # Fixed: is_alive → alive
                    target = (monster.x, monster.y)
                    break
        
        # Monsters hunt predators
        if isinstance(agent, Monster):
            closest_predator = None
            closest_dist = float('inf')
            for pred in self.predators:
                if pred.alive:  # Fixed: is_alive → alive
                    dist = MovementSystem.manattan_distance((agent.x, agent.y), (pred.x, pred.y))  # Fixed typo
                    if dist < closest_dist:
                        closest_dist = dist
                        closest_predator = pred
            if closest_predator:
                target = (closest_predator.x, closest_predator.y)
        
        # If we have a target, move toward it
        if target:
            success = MovementSystem.move_towards_target(agent, target, self.grid)  # Fixed typo
            if success and isinstance(agent, Predator):
                agent.useStamina(5)  # Fixed: 100 → 5
            return success
        
        # Fallback: random movement if no target
        return self._move_agent_random(agent)
        
    def _move_agent_random(self, agent: Agent):
        """Move an agent to a random adjacent position."""
        if not agent.alive:
            return False
        
        # Random direction
        dx = random.choice([-1, 0, 1])
        dy = random.choice([-1, 0, 1])
        
        new_x = agent.x + dx
        new_y = agent.y + dy
        
        return self.grid.move_agent(agent, new_x, new_y)
    
    def _check_combat(self, agent: Agent):
        """Check if agent is adjacent to an enemy and initiate combat."""
        if not agent.alive:
            return

       
        
        # Check adjacent cells
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
                
                # Determine if they're enemies
                if isinstance(agent, Predator) and isinstance(target, Monster):
                    self._resolve_combat(agent, target)
                elif isinstance(agent, Monster) and isinstance(target, Predator):
                    self._resolve_combat(target, agent)
                elif isinstance(agent, Predator) and isinstance(target, Synthetic):
                    # Predators might attack synthetics
                    if random.random() < 0.3:  # 30% chance
                        self._resolve_combat(agent, target)
    
    def _resolve_combat(self, attacker: Agent, defender: Agent):
        """Resolve combat between two agents."""
        if not attacker.alive or not defender.alive:
            return
        
        self.stats['combats'] += 1
        
        # Calculate damage
        if isinstance(attacker, Monster):
            damage = attacker.damage
        elif isinstance(attacker, Predator):
            damage = random.randint(20, 40)  # Predator damage
        else:
            damage = random.randint(10, 20)  # Synthetic damage
        
        # Apply damage
        still_alive = defender.take_damage(damage)
        
        print(f"  ⚔️  {attacker.name} attacks {defender.name} for {damage} damage!")
        
        if not still_alive:
            self.stats['deaths'] += 1
            print(f"  💀 {defender.name} has been defeated!")
            
            # Remove from grid
            self.grid.remove_agent(defender)
            
            # Track kills
            if isinstance(attacker, Predator):
                attacker.record_kill()
                attacker.gain_honour(10)
                self.stats['kills'] += 1
            
            # Remove from active lists
            if isinstance(defender, Predator) and defender in self.predators:
                self.predators.remove(defender)
            elif isinstance(defender, Monster) and defender in self.monsters:
                self.monsters.remove(defender)
            elif isinstance(defender, Synthetic) and defender in self.synthetics:
                self.synthetics.remove(defender)
    
    def _update_agents(self):
        """Update all agents (movement, combat, etc.)."""
        # Shuffle to randomize turn order
        random.shuffle(self.all_agents)
        
        for agent in self.all_agents[:]:  # Copy list to avoid modification issues
            if not agent.alive:
                continue
            
            # Move agent
            if random.random() < 0.7:  # 70% chance to move
                self._move_agent_smart(agent)
            
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
        """
        Run the simulation.
        
        Args:
            display_every: Display grid every N turns (0 to disable)
            max_turns: Maximum number of turns to run
        """
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
        print(f"  Turn: {self.turn}")
        print(f"  Alive - Predators: {alive_predators}, Monsters: {alive_monsters}, Synthetics: {alive_synthetics}")
        print(f"  Combats: {self.stats['combats']}, Kills: {self.stats['kills']}, Deaths: {self.stats['deaths']}")
        
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
    """Main entry point for the simulation."""
    # Create simulation
    sim = Simulation(
        width=20,
        height=20,
        num_predators=3,
        num_monsters=5,
        num_synthetics=2
    )
    
    # Test scan functionality
    sim.test_scan()
    
    # Run simulation
    sim.run(display_every=10, max_turns=50)
    
    print("\n✅ Simulation complete!")


if __name__ == "__main__":
    main()

