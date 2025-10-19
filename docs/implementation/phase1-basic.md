# Design Decisions Log

## Phase 1: Basic Implementation (Week 1)

### Overview
Completed requirements a) and b) from the brief:
- Environment Grid (20×20 with wrapping)
- Predator Agents (Dek with health, stamina, honour) 
- Boss and monster enetities added. Also inherits from the agent class

---

### Decision: Grid Structure - 2D List
**Date:** Oct 12, 2025
**What:** Implemented grid as `list[list[Agent|None]]` (2D list)
**Why:** 
- 20×20 is small (only 400 cells) - memory not a concern
- O(1) access time for spatial queries
- Simple to visualise and debug
- Easy to display in terminal

**Alternative Considered:** Dictionary with (x,y) tuples as keys (sparse grid)
**Why Rejected:** 
- Overkill for small, densely-populated grid
- Would add complexity without performance benefit
- 2D list is more intuitive for grid-based simulation



---

### Decision: Grid Wrapping Using Modulo
**Date:** Oct 12, 2025
**What:** Position wrapping implemented with `x % width, y % height`
**Why:**
- Requirement explicitly states: "The grid should wrap around at the edges"
- Simulates continuous planetary terrain without boundaries
- Prevents agents getting stuck in corners
- Modulo operator elegantly handles both positive and negative overflow

**Example:**
-p ython

- normalise_position(21, 5) 
- normalise_position(-1, 10) 





**Date:** Oct 12, 2025
**What:** Created base `Agent` class, extended by `Predator`
**Why:**
- Follows DRY principle - shared attributes (health, position) in one place
- Makes adding new agent types (Monster, Synthetic) easier
- Supports polymorphism - can treat all agents uniformly in collections

**Inheritance Hierarchy:**
```
Agent (base)
  ├── Predator (Dek, father, brother, clan)
  ├── Monster (to be implemented)
  └── Synthetic (Thia - to be implemented)
```

**Code Location:** `src/entities/agent.py`, `src/entities/predator.py`

---

### Decision: Predator Symbol Differentiation
**Date:** Oct 12, 2025
**What:** Dek uses 'D' symbol, other predators use 'P'
**Why:**
- Easy to identify the main character in simulation
- Requirement distinguishes between Dek and clan members
- Helps with debugging and visualisation

**Implementation:**
```python
symbol = 'D' if is_dek else 'P'
```

**Code Location:** `src/entities/predator.py` - constructor

---

### Decision: Honour Scale 0-100
**Date:** Oct 12, 2025
**What:** Honour represented as integer 0-100 with rank descriptions
**Why:**
- Simple, intuitive scale
- Easy to calculate percentage-based changes
- Rank descriptions (Disgraced, Dishonoured, Neutral, Honoured, Legendary) provide narrative context

**Trade-off:** Could use more granular system, but 0-100 sufficient for simulation needs

**Code Location:** `src/entities/predator.py` - `get_honour_rank()` method

------------------------------------------------------------------------------------

## Phase 1 Extended: Agent Classes Complete

### Decision: Synthetic Scanning Ability
**Date:** Oct 12, 2025
**What:** Implemented `scan_area()` method for Synthetic class
**Why:**
- Requirement c states Thia can provide "knowledge or clues" and do "reconnaissance"
- Gives Thia a unique, useful role beyond being carried
- Enables multi-agent coordination - Dek can use Thia's intel for decisions
- Sets up foundation for AI decision-making (agents can gather information about environment)

**Implementation Details:**
- Scans in configurable radius (default 3 cells)
- Returns structured data: monsters, predators, other synthetics
- Calculates Manhattan distance for each detected agent
- Distinguishes between regular monsters and boss (ultimate adversary)
- Uses `isinstance()` checks for type safety and IDE autocomplete

**Design Choice - Structured Return Data:**
Returns dictionary with detailed info rather than just agent names:
```python
{
    'monsters': [{'name': '...', 'position': (x,y), 'distance': n, 'health': h}],
    'predators': [...],
    'boss': {...} or None,
    'threats_detected': count
}
```
**Rationale:** Other agents (especially Dek's AI) need actionable data to make decisions, not just names.

**Code Location:** `src/entities/synthetics.py` - `scan_area()` method


---
### Things I have learned and bugs fixed.
### Decision: isinstance() vs String Type Checking
**Date:** Oct 12, 2025
**What:** Used `isinstance(obj, ClassName)` instead of `type(obj).__name__ == "ClassName"`
**Why:**
- More Pythonic and robust
- Enables IDE autocomplete/intellisense
- Handles inheritance correctly
- Faster performance
- Clearer intent

**Example:**
```python
# Better
if isinstance(cell_content, Monster):
    cell_content.is_boss  # IDE knows available attributes

# vs. worse
if type(cell_content).__name__ == "Monster":
    cell_content.is_boss  # IDE doesn't know what attributes exist
```

---

### Bug Fix: Loop Early Return
**Date:** Oct 12, 2025
**Problem:** `scan_area()` only checking one cell instead of full range
**Cause:** `return scan_results` was indented inside the loop instead of after it
**Solution:** Moved return statement to correct indentation level (aligned with `for` loop)
**Lesson:** Those rookie errors still trip me up from time to time. Easy to accidentally put `return` inside loop when it should be after

---

### Bug Fix: Grid Wrapping in Scan
**Date:** Oct 12, 2025
**Problem:** Scan was detecting Thia's own position at (-5, -5) when she's at (5, 5)
**Cause:** Grid wrapping means negative coordinates wrap around. On 10×10 grid, (-5, -5) wraps to (5, 5)
**Solution:** Skip check when `dx=0 and dy=0` (checking own position) happens before calculating wrapped position
**Lesson:** Grid wrapping affects spatial queries - need to account for this in scanning logic

---

## Current Implementation Status

**Completed Requirements:**
- ✅ a) Environment Grid (20×20, wrapping, agent placement/movement)
- ✅ b) Predator Agents (Dek with health, stamina, honour, kill tracking)
- ✅ c) Synthetic Androids (Thia with damaged state, reconnaissance via scanning)
- ✅ d) Monster Threat (regular monsters and boss with higher health/damage)
- ⏳ e) Clan & Social Mechanics (not yet implemented)
- ⏳ f) Survival & Resource Constraints (partial - have stamina, need to add resource depletion)
- ⏳ g) Simulation Dynamics (not yet implemented)

**Current Grade Target:** 50-59% (2:2) requirements mostly met, will attemptp e next and start the phase 2 documentation process.

**Agent Classes Completed:**
- `Agent` (base class)
- `Predator` (Dek, father, brother, clan members)
- `Monster` (creatures and ultimate adversary)
- `Synthetic` (Thia with scanning capability)

**Git Commits:** 7-8 commits with meaningful messages

---

## Next Steps

**Immediate (to reach 60-69%):**
1. Implement basic combat system (requirement f, g)
2. Add simple rule-based AI for Dek's decision-making (requirement b, g)
3. Create simulation loop that runs multiple turns (requirement g)
4. Add clan mechanics - father/brother agents with patrol behavior (requirement e)

**Medium-term (to reach 70-79%):**
1. Implement full honour/reputation system with clan reactions (requirement e)
2. Add resource constraints (stamina depletion, carrying penalties) (requirement f)
3. Implement pathfinding for intelligent movement
4. Add environmental hazards

**Long-term (to reach 80-100%):**
1. Implement reinforcement learning (requirement h)
2. Multi-agent coordination between Dek and Thia (requirement h)
3. Adaptive adversary that learns from player strategies (requirement h)
4. Procedural generation of hazards (requirement h)
5. Run 20+ experiments with statistical analysis (requirement h)
-THE END GOAL

---

## Time Tracking

**Phase 1 Time Spent:** ~4 hours
- Grid implementation: 1 hour
- Agent classes: 1.5 hours
- Synthetic scanning: 1 hour
- Debugging and testing: 0.5 hours

**Remaining Time:** 96 days (as of Oct 12, 2025)
**On Track:** Yes - have foundation complete with plenty of time for advanced features, feeling pretty on top of things.
