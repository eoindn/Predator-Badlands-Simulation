## Phase 4: Reinforcement Learning Implementation

### Overview
**Session Duration:** Ongoing

This phase implements Q-learning reinforcement learning for Dek to enable adaptive decision-making that improves over time through experience.

---

## Design Decisions Log - Reinforcement Learning Implementation

### Decision: Q-Learning Algorithm Choice
**Date:** December 2026
**What:** Implemented Q-learning algorithm for Dek's decision-making
**Why:**
- Requirement h calls for adaptive AI that learns from experience
- Q-learning is well-suited for discrete state/action spaces like our grid-based simulation
- Allows Dek to improve strategies over multiple simulation runs
- Balance between exploration and exploitation

**Implementation:**
- Q-table stores state-action value pairs
- Epsilon-greedy action selection for exploration/exploitation balance
- Learning rate (alpha) controls how quickly knowledge updates
- Discount factor (gamma) determines importance of future rewards

**Code Location:** `src/ai/reinforcement.py`



### Decision: State Representation
**Date:** December 2026
**What:** State represented as tuple of discrete categories
**Why:**
- Discrete states work better with Q-learning than continuous values
- Reduces state space size (prevents Q-table explosion)
- Categories capture essential game information

**State Components:**
- Health state: 'high' (>65), 'medium' (30-65), 'low' (<30)
- Stamina state: 'high' (>65), 'low' (≤65)
- Honour state: 'high' (>50), 'medium' (20-50), 'low' (<20)
- Threat level: 'high' (≥3 nearby), 'medium' (2), 'low' (0-1)

**Trade-off:** Less granular than continuous values, but enables learning with reasonable table size

---

### Decision: Action Space
**Date:** December 2026
**What:** Six actions for Dek
**Actions:**
- `hunt_monster` - Attack regular monsters
- `hunt_boss` - Attack the ultimate adversary
- `collect_resource` - Gather resources
- `rest` - Recover stamina
- `seek_thia` - Find and assist Thia
- `avoid_danger` - Move away from threats

**Why:**
- Covers main strategic options Dek faces
- Discrete actions match Q-learning requirements
- Balance between combat, survival, and resource management

---

### Decision: Reward Structure
**Date:** December 2026
**What:** Reward system that encourages positive outcomes

**Positive Rewards:**
- Killed boss: +100 (major achievement)
- Killed monster: +20
- Gained honour: +10
- Collected resource: +5
- Healed: +3

**Neutral:**
- Moved: 0

**Negative Rewards:**
- Wasted action: -2
- Took damage: -10
- Lost honour: -15
- Died: -100 (major penalty)

**Why:**
- Rewards guide learning toward survival and honour maintenance
- Large penalties for death encourage survival strategies
- Positive rewards for combat success encourage engagement
- Honour rewards reinforce clan code adherence


### Decision: Q-Table Persistence
**Date:** December 2026
**What:** Save/load Q-table using pickle
**Why:**
- Allows learning to persist across simulation runs
- Enables cumulative learning over multiple experiments
- Essential for demonstrating improvement over time

**Code Location:** `src/ai/reinforcement.py` - `save()` and `load()` methods

---

## Implementation Status

**Completed:**
- Qlearning class structure
- State representation system
- Action selection (epsilon-greedy)
- Qvalue update mechanism
- Reward function
- Qtable persistence



**Future Work:**
- State space refinement based on results
- Reward function tuning
- Performance evaluation vs rule-based system
- Multi-agent coordination with Thia

## Integration with Simulation

**Current Integration Point:**
- `_dek_q_learning_actions()` method in `simulation.py`
- Gets current state from Q-table
- Chooses action based on epsilon-greedy policy


## Expected Outcomes

**Learning Goals:**
- Dek should improve survival rate over multiple runs
- Better resource management strategies
- More effective combat decisions
- Honour conscious decision-making

**Evaluation Metrics:**
- Survival rate improvement over runs
- Average honour scores
- Boss defeat rates
- Resource utilisation efficiency



## Challenges and Limitations


- State space may need refinement based on initial results
- Reward function may need tuning
- Exploration vs exploitation balance
- Integration complexity with existing simulation systems
- Discrete state representation loses some nuance
- Fixed reward values may not capture all strategic subtleties
- Learning requires many simulation runs to show improvement
- Current implementation doesn't handle Thia coordination yet

