import heapq
from typing import List, Tuple, Optional, Set
from core.grid import Grid
from entities.agent import Agent

class PathNode:

    def __init__(self, position: Tuple[int, int], g_cost: float, h_cost: float, parent: Optional['PathNode'] = None):
        self.position = position
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


class MovementSystem:

    @staticmethod
    def manattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def eucilidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    @staticmethod
    def get_neighbors(position: Tuple[int, int], grid: Grid, allow_diagonal: bool = True) -> List[Tuple[int, int]]:
        x, y = position
        neighbors = []

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        if allow_diagonal:
            directions.extend([(1, 1), (1, -1), (-1, -1), (-1, 1)])

        for dx, dy in directions:
            new_x = (x + dx) % grid.width
            new_y = (y + dy) % grid.height
            neighbors.append((new_x, new_y))
    
        return neighbors

    @staticmethod
    def a_star_search(start: Tuple[int, int], goal: Tuple[int, int], grid: Grid,
                      avoid_agents: bool = False) -> Optional[List[Tuple[int, int]]]:

        if start == goal:
            return [start]

        open_set = []
        start_node = PathNode(start, 0, MovementSystem.manattan_distance(start, goal))
        heapq.heappush(open_set, start_node)

        closed_set: Set[Tuple[int, int]] = set()
        g_costs = {start: 0}

        while open_set:
            current = heapq.heappop(open_set)

            if current.position == goal:
                path = []
                node = current
                while node:
                    path.append(node.position)
                    node = node.parent
                return list(reversed(path))

            if current.position in closed_set:
                continue

            closed_set.add(current.position)

            for neighbor_pos in MovementSystem.get_neighbors(current.position, grid):
                if neighbor_pos in closed_set:
                    continue
                
                if avoid_agents and neighbor_pos != goal:
                    cell_agent = grid.get_cell(neighbor_pos[0], neighbor_pos[1])
                    if cell_agent is not None:
                        continue

                move_cost = 1.4 if abs(neighbor_pos[0] - current.position[0]) + abs(neighbor_pos[1] - current.position[1]) == 2 else 1.0
                tentative_g = current.g_cost + move_cost

                if neighbor_pos not in g_costs or tentative_g < g_costs[neighbor_pos]:
                    g_costs[neighbor_pos] = tentative_g
                    h_cost = MovementSystem.manattan_distance(neighbor_pos, goal)
                    neighbor_node = PathNode(neighbor_pos, tentative_g, h_cost, current)
                    heapq.heappush(open_set, neighbor_node)
        
        return None

    @staticmethod
    def get_next_move(agent: Agent, target_pos: Tuple[int, int], grid: Grid) -> Optional[Tuple[int, int]]:
        current_pos = (agent.x, agent.y)
        path = MovementSystem.a_star_search(current_pos, target_pos, grid, avoid_agents=True)

        if path and len(path) > 1:
            return path[1]

        return None

    @staticmethod
    def move_towards_target(agent: Agent, target_pos: Tuple[int, int], grid: Grid) -> bool:
        next_pos = MovementSystem.get_next_move(agent, target_pos, grid)
        if next_pos:
            return grid.move_agent(agent, next_pos[0], next_pos[1])
        return False

    @staticmethod 
    def move_towards_target(agent: Agent, target_pos: Tuple[int, int], grid: Grid) -> bool:
        next_pos = MovementSystem.get_next_move(agent, target_pos, grid)
        if next_pos:
            return grid.move_agent(agent, next_pos[0], next_pos[1])
        return False
