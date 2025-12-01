## Phase 3 : Clan Dynamics(honor and reputation) and Simulation Changes

### Overview
**Date written** Dec 1, 2025
**Session Duration** About 4 hours




# Design Decisions Log - Comprehensive Implementation (2:1 Grade)

## Project Status: Upper Second Class (60-69%)

**Date:** December 1, 2025
**Requirements Met:** a through e fully implemented

Completed:
- Intelligent path finding
- Social Clan mechanics 
- Honor system 
- Weather System 


## Requirements Completion Summary



### ✅ Requirement Clan & Social Mechanics - COMPLETE


**Implementation:**
- Clan hierarchy with distinct roles 
- Honour based attitude system with 5 levels (Hostile disapproving, neutral, approving, respectful)
- Dynamic dialogue thfat changes based on Dek's honour
- Challenge system where clan members confront Dek

**How I implemented the clan hierarchy implementation:**

**Father:**
- Honour less than 20: "You disgrace our bloodline! Leave and never return!"
- Honour 20-39: "Prove yourself worthy, or remain exiled forever."
- Honour 40-59: "Show me you have our blood, runt."
- Honour 60-79: "You begin to show promise, my son."
- Honour 80+: "You have earned your place. Welcome back, warrior."

**Brother (Warrior Role):**
- More aggressive and mocking tone
- Challenges Dek more frequently

**Design Decision - Honour Thresholds:**


**Honour Gain/Loss System:**
Actions that increase honour:
- Kill monster: +10
- Kill boss: +30
- Save ally: +15
- Complete hunt: +5

Actions that decrease honour:
- Flee combat: -15
- Attack weak/injured: -20 (this violates Yautja code)
- Abandon ally: -25
- Refuse challenge: -10

**Design Rationale:** Values where calibrated in a way so that 3-4 monster kills wouod move Dek from "exile" to "neutral" status

**Challenge System:**
Clan members call `challenge_dek(dek, grid)` each turn which does the following things :
- Checks Dek's honour level
- Issues verbal challenge or approval based on honour
- Low honour results in blocking and hostile dialogue
- High honour results acceptance and respectful dialogue

**Code Location:** 
- `src/entities/predator.py` 
- `get_clan_status()`, `clan_dialogue()`
-  `challenge_dek()`
- `src/core/simulation.py` 
- Challenge system integrated in `_update_agents()`



## Some Additional Systems Implemented

### A* Pathfinding (Movement System)
- I Touched on this in detail in the previous document however, I believe its worth mentioning again due to its complexity.

**What I have done :** Implemented A* algorithm for intelligent agent movement
**Why?:** Requirement for advanced AI behavior - agents find optimal paths to targets
**How It Works:**
- Uses Manhattan distance heuristic (appropriate for grid-based movement)
- Considers grid wrapping for shortest path calculation
- Predators path toward boss, monsters path toward nearest predator



**Design Decision - Manhattan vs Euclidean Distance:**
**Chose:** Manhattan distance
**Why:** Agents move in cardinal directions only (no diagonal movement), so Manhattan distance accurately represents actual movement cost
**Alternative:** Euclidean distance
**Rejected:** Would underestimate path length, leading to suboptimal pathfinding

**Code Location:** `src/systems/movement.py`

---

### Weather/Environmental Hazard System
**What:** Random weather effects applied to Dek every 5 turns
**Why:** Satisfies requirement "Environmental hazards impose additional cost"


**Weather Effects:**
- Hot: -20 stamina (like exhaustion from heat)
- Cold: -5 health (exposure damage)
- Rainy: Sets encumbered flag (movement penalty)
- Thunder Storm: -15 health (lightning/severe weather damage)






**Design Decision - Apply to Dek Only:**

**What:** Weather affects protagonist (Dek) but not all agents
**Why:** 
- Creates asymmetric challenge for player agent
- Avoids effecting all agents which could stall the game
- Focuses resource pressure on decision making agent

**Frequency:** Every 5 turns (20% of turns affected)

**Code Location:** `src/core/simulation.py` - `weather_system()`

---

### Combat System
**What:** Adjacent agents engage in combat with damage resolution method
**Why:** Core interaction mechanic for simulation dynamics

**Combat Resolution:**
1. Check adjacent cells in 8 directions for enemy agents
2. A 40% chance for enemy to initiate combat
3. Calculate damage based on attacker type
4. Apply damage and check for death
5. Award honour and track kills for predators, brother/dek relationship relies on this partially

**Damage Values:**
- Predators: 20-40 (random, to represent a varience in skil)
- Monsters: 10-15 and 30 for the boss
- Synthetics: 10-20

**Design Decision**
 - Probabilistic Combat


**What:** Only 40% chance to attack adjacent enemy per turn
**Why:** 
- Prevents every adjacent encounter becoming instant combat
- Allows agents to move past each other occasionally
- Creates more dynamic movement patterns
- Reduces simulation stalemate where agents spam attack same target

**Kill Tracking:**
Each Predator has a killd attribute which i sincremented on a successful kill
- Displayed in statistics output
- Can be used for achievement systems or AI decisions
- Provides metric for agent performance evaluation

**Code Location:** `src/core/simulation.py` - `_check_combat()`, `_resolve_combat()`

---


### Current Implementation Status

**Completed Requirements:**
- ✅ a) Environment Grid
- ✅ b) Predator Agents with pathfinding
- ✅ c) Synthetic Androids (Thia with scanning)
- ✅ d) Monster Threat (boss with 500 HP)
- ✅ e) Clan Mechanics - **PARTIAL** (with Yautja Code)
- ✅ f) Resource Constraints - **PARTIAL** (stamina implemented, need environmental hazards, this was added quite early)
- ⏳ g) Simulation Dynamics - **IN PROGRESS** (not really, need more smart behaviour but the basic loop works)

### Next Steps (Phase 4)
1. Smarter behaviour, need more actions such as carrying , repairing etc
2. Thia and Dek must collaborate and share information
3. Literally everthing in the expert level challenge
4. Smarter decision making methods , using ai algorithms or behaviour trees.

**Time Remaining:** 38 days!


