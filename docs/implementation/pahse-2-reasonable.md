## Phase 2: Pathfinding & Clan Mechanics (Week 5)

### Overview
**Date:** Nov 23, 2025
**Session Duration:** many hours since I had taken a hiatus from the project to focus on other ones
**Goal:** Implement intelligent movement and clan social dynamics

Completed:
- A* pathfinding system
- Intelligent agent movement (predators hunt boss, monsters hunt predators)
-Stamina resource management
- Father and Brother clan characters with challenge system
- Combat balancing

**Current Status:** Requirements a-d complete, e & f partial.


### Decision: A* Pathfinding Algorithm
**Date:** Nov 21, 2025
**What:** Implemented A* in `MovementSystem` class for intelligent navigation
**Why:**
- Requirement g needs agents to "choose actions intelligently"
-random movement wasn't strategic enough and agents need to seek goals
- A* finds shortest path while avoiding obstacles


**How it Works:**
- Uses Manhattan distance as heuristic 
- Priority queue (heapq) to find promising paths first
- Tracks visited nodes to avoid cycles
- iagonal moves cost 1.4, orthogonal moves cost 1.0 (realistic movement)

**Alternatives that I Considered:**
- BFS: Too slow, explores uniformly without heuristic
- Dijkstra's: Slower than A* (no heuristic guidance)

**Code Location:** `src/systems/movement.py`

---

### Decision: Separate MovementSystem Class
**Date:** Nov 23, 2025
**What:** Created `MovementSystem` with static methods



**Why:**
- Single Responsibility Principle - movement logic separate from agent logic
- Multiple agent types can share pathfinding
- Easier to test and debug in isolation


**Key Methods:**
- `a_star_search()` - Core pathfinding algorithm
- `move_toward_target()` - for one-step movement since the simulation runs in an iteration of singular turns
- `manhattan_distance()`, `euclidean_distance()` - Distance metrics

---

### Decision: Clan Challenge System with Cooldown
**Date:** Nov 23, 2025
**What:** Father and Brother challenge Dek based on honour/performance, with 10-turn cooldown which i added due to a bug
**Why:**
- Requirement e needs "clan hierarchy" and "internal conflict"
- Creates a sens of narrative tension - Dek must prove himself to family
- Cooldown prevents spam (Father was challenging on every turn)

**Challenge Triggers:**
- **Father:** Challenges if Dek's honour < 60
- **Brother:** Challenges if Dek has 2+ more kills (a kind of jealousy mechanic)
- Both require distance ≤ 2 cells (must be nearby other wise the output would start going crazy)

**Bugs Fixed:**
- Initial conditions too strict (Father < 40 honour, Brother +2 kills) nobody challenged as a result of this
- No cooldown caused message spam as mentioned earlier so added 10-turn cooldown
- Dek's honour could go negative had to cap it

**Code Location:** `src/entities/predator.py` - `challenge_dek()` method

---

### Decision: Stamina Costs for Movement
**Date:** Nov 23, 2025
**What:** Predators spend 5 stamina per move, regenerate 10 when resting
**Why:**
- Requirement f needs "energy/stamina that depletes with movement"
- Creates resource management since its unrealistic to move forever
- Forces strategic decisions 
- Balances combat 

**Values Chosen:**
- Cost: 5 stamina per move (20 moves before exhaustion)
 Regen: 10 stamina per rest turn (2 turns to fully recover from 1 move)
- Max: 100 stamina

**Bugs Fixed:**
- Initially drained 100 stamina per move - agents couldn't move after first step!
- Changed to 5 stamina for balance

**Code Location:** `src/simulation.py` - `_move_agent_smart()` method

---

### Decision: Combat Frequency Balancing
**Date:** Nov 23, 2025
**What:** 30% chance per adjacent enemy per turn to initiate combat
**Why:**
- Initial version attacked ALL adjacent enemies EVERY turn - boss died in 10 turns
- Combat was too fast so there was no strategy involved
- 30% creates more realistic attakcs rather than guaranteed combat all the time

**Boss Balancing:**
- Boss health: 500 HP (vs 100 for regular monsters)
- Boss damage: 50 (vs 30 for regular monsters)
- Makes boss an actual challenge requiring multiple predators cooperating it was 350 before

**Code Location:** `src/simulation.py` - `_check_combat()` method

---

### Bugs Fixed This Session



**Bug:** 100 Stamina Drain
- **Problem:** Movement cost 100 stamina instead of 5
- **Fix:** Changed to 5 stamina per move

**Bug:** Combat Spam
- **Problem:** Combat triggered for all adjacent enemy
- **Cause:** Random check was outside neighbor loop
- **Fix:** Moved random check inside loop (30% per enemy)

**Bug:** Overlapping Spawn Positions
- **Problem:** Father and Brother spawning at same location
- **Cause:** Reused same `(x, y)` position
- **Fix:** Call `_find_empty_position()` for each agent

---

### Current Implementation Status

**Completed Requirements:**
- ✅ a) Environment Grid
- ✅ b) Predator Agents with pathfinding
- ✅ c) Synthetic Androids (Thia with scanning)
- ✅ d) Monster Threat (boss with 500 HP)
- ⏳ e) Clan Mechanics - **PARTIAL** (challenges work, need Yautja Code)
- ⏳ f) Resource Constraints - **PARTIAL** (stamina implemented, need environmental hazards)
- ⏳ g) Simulation Dynamics - **IN PROGRESS** (basic loop works)

**Git Commits:** ~15 commits total (added ~7 this session)

---

### Lessons Learned

1. **A* is Complex:** This took a long time to understand properly. Breaking it into steps helped but this was very challenging and required good theory
2. **Balancing is Iterative:** Boss health, combat frequency, stamina costs all needed tuning.
3. **Small Bugs Compound:** Typos like `is_alive` vs `alive` broke entire movement system.
4. **Debug Early:** Adding print statements showed why challenges weren't firing.
5. **Cooldowns Matter:** Any repeating event needs cooldown to prevent spam.

---

### Next Steps (Phase 3)

**To reach 60-69% (Upper Second):**
1. Implement Yautja honour Code enforcement (don't attack weak enemies)
2. Dek carries Thia mechanic with movement penalty
3. Environmental hazards (traps, hostile terrain)

**To reach 70-79% (First Class):**
4. Full decision-making system (state machines or behavior trees)
5. Thia provides strategic intel that Dek uses
6. Win condition: Dek defeats boss and restores honour

lots to do forsure

**Current Target:** Finish requirement e) completely (Yautja Code + full clan dynamics)

**Time Remaining:** 50 days