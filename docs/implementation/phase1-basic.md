# Design Decisions Log

## Phase 1: Basic Implementation (Week 1)

### Overview
Completed requirements a) and b) from the brief:
- Environment Grid (20×20 with wrapping)
- Predator Agents (Dek with health, stamina, honour)

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
```python
# 20x20 grid
normalise_position(21, 5)  # Returns (1, 5) - wraps right to left
normalise_position(-1, 10) # Returns (19, 10) - wraps left to right