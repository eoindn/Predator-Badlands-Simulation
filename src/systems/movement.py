import heapq
from typing import List,Tuple,Optional, Set
from core.grid import Grid
from entities.agent import Agent

class PathNode:

    def __init__(self,position:Tuple[int,int], g_cost: float, h_cost: float, parent: Optional['PathNode'] = None):
        self.position = position
        self.g_cost = g_cost # saying how much it costs to get here from the start
        self.h_cost = h_cost  # estimated cost to get from here to the goal
        self.f_cost = g_cost + h_cost # this is the total estimated cost
        self.parent = parent # this is the node we came from which is used for reconstructing

    def __lt__(self, other):
        return self.f_cost < other.f_cost


    def __eq__(self,other):
        return self.position == other.position


    def __hash__(self):
        return hash(self.position)



class MovementSystem:

    @staticmethod
    def manattan_distance(pos1: Tuple[int,int], pos2: Tuple[int,int]) -> int:

        # calculating manhattan distance between two positions
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        #defining what mahattan distance is
        # Manhattan distance = like a city block distance where you can only move up/down/left/right (akin to walking on a grid of streets).

    @staticmethod ## going to be useufl for thias scan range , simulating a circular scan or for combat range
    def eucilidean_distance(pos1 : Tuple[int,int], pos2: Tuple[int,int]) -> float:
        return (( pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])   ** 2) ** 0.5



    @staticmethod
    def get_neighbors(position: Tuple[int,int], grid: Grid, allow_diagonal: bool = True) -> List[Tuple[int,int]]:

        x,y = position
        neighbors = []

        directions = [(0,1),(1,0),(0,-1),(-1,0)] # directions for up down left right

        if allow_diagonal:
            directions.extend([(1,1),(1,-1),(-1,-1),(-1,1)])

        for dx, dy in directions:
            new_x = (x + dx) % grid.width  # Wrap around
            new_y = (y + dy) % grid.height
        
            neighbors.append((new_x, new_y))
    
        return neighbors


    @staticmethod
    def a_star_search(start :Tuple[int,int], goal: Tuple[int,int], grid:Grid,
        avoid_agents: bool = False) -> Optional[List[Tuple[int,int]]]:

        if start == goal:
            return [start]

        open_set = [] #priority queuue for nodes to explore


        start_node = PathNode(start, 0, MovementSystem.manattan_distance(start,goal)) #manhattan distance for h cost
        heapq.heappush(open_set,start_node)


        #track visited nodes
        closed_set: Set[Tuple[int,int]] = set()

        # need to track the best g_cost to reach each position 
        g_costs = {start: 0}

         # main loop

        while open_set:
            current = heapq.heappop(open_set)

            if current.position == goal: # W weve reached the goal

            #reconstruc the path with the parent links

                path = []
                node = current


                while node:
                    path.append(node.position)
                    node = node.parent

                return list(reversed(path))

            if current.position in closed_set:
                continue #means weve already had a look at this node so we skip that

            closed_set.add(current.position)

            #xplore the neighbors
            for neighbor_pos in MovementSystem.get_neighbors(current.position, grid):
                if neighbor_pos in closed_set:
                    continue
                
                # check to avoid this cell if its not empty (but allow goal cell)
                if avoid_agents and neighbor_pos != goal:
                    cell_agent = grid.get_cell(neighbor_pos[0], neighbor_pos[1])
                    if cell_agent is not None:
                        continue
                
                #calculate costs
                move_cost = 1.4 if abs(neighbor_pos[0] - current.position[0]) + abs(neighbor_pos[1] - current.position[1]) == 2 else 1.0
                tentative_g = current.g_cost + move_cost

                #check if its an ideal path
                if neighbor_pos not in g_costs or tentative_g < g_costs[neighbor_pos]:
                    g_costs[neighbor_pos] = tentative_g
                    h_cost = MovementSystem.manattan_distance(neighbor_pos, goal)
                    neighbor_node = PathNode(neighbor_pos, tentative_g, h_cost, current)
                    heapq.heappush(open_set, neighbor_node)
        
        return None  # No path found



 
    @staticmethod
    def get_next_move(agent: Agent, target_pos : Tuple[int,int], grid: Grid) -> Optional[Tuple[int,int]]:

        current_pos = (agent.x, agent.y)
        path = MovementSystem.a_star_search(current_pos, target_pos, grid, avoid_agents = True)

        if path and len(path) > 1:
            return path[1]

        return None

    @staticmethod
    def move_towards_target(agent:Agent, target_pos:Tuple[int,int], grid:Grid) -> bool:

        next_pos = MovementSystem.get_next_move(agent, target_pos,grid)

        if next_pos:
            return grid.move_agent(agent, next_pos[0],next_pos[1])

        return False

    


    @staticmethod
    def move_towards_target(agent:Agent, target_pos:Tuple[int,int], grid:Grid) -> bool:

        next_pos = MovementSystem.get_next_move(agent, target_pos,grid)

        if next_pos:
            return grid.move_agent(agent, next_pos[0],next_pos[1])

        return False




