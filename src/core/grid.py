class Grid:
    """
    2D grid environment representing planet Kalisk.
    
    Grid wraps around at edges to simulate vast terrain.
    Each cell can contain one agent or be empty.
    """
    
    def __init__(self, width=20, height=20):
        """
        Initialize empty grid.
        
        Args:
            width: Grid width (default 20 per requirements)
            height: Grid height (default 20 per requirements)
        """
        self.width = width
        self.height = height
        # 2D list - each cell is None (empty) to start
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        
    
    def normalize_position(self, x, y):
        """
        Wrap coordinates around grid edges.
        
        Returns:
            tuple: (x, y) wrapped to valid grid coordinates
        """
        return x % self.width, y % self.height
    
    def is_valid_position(self, x, y):
        """
        Check if position is within grid bounds.
        
        Returns:
            bool: True if position is in range
        """
        return 0 <= x < self.width and 0 <= y < self.height
    
    def display(self):
        """Print grid with agents."""
        print("\n" + "=" * (self.width * 2 + 1))
        for row in self.grid:
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    line += cell.symbol + " "
            print(line)
        print("=" * (self.width * 2 + 1) + "\n")

    def is_empty(self, x, y):
        
        x, y = self.normalize_position(x, y)
        return self.grid[y][x] is None

    def get_cell(self, x, y):
        
        x, y = self.normalize_position(x, y)
        return self.grid[y][x]

    def place_agent(self, agent, x, y):
        
        x, y = self.normalize_position(x, y)
        
        if not self.is_empty(x, y):
            return False
        
        self.grid[y][x] = agent
        agent.x = x
        agent.y = y
        return True

    def remove_agent(self, agent):
       
        if 0 <= agent.y < self.height and 0 <= agent.x < self.width:
            self.grid[agent.y][agent.x] = None

    def get_position(self):
        return (self.x, self.y)


    def weather_system(self):
        weather = {
                1:"hot",
                2:"cold",
                3:"rainy",
                4:"thunder_storm"}

        
        keys = list(weather.keys())

        random_key = random.choice(keys)

        random_weather_value = weather[random_key]

        return random_weather_value
            

    

    

    def move_agent(self, agent, new_x, new_y):
        """
        Move an agent to a new position.
        
        Args:
            agent: Agent to move
            new_x, new_y: Destination coordinates
            
        Returns:
            bool: True if moved successfully, False if destination occupied
        """
        new_x, new_y = self.normalize_position(new_x, new_y)
        
        #
        if not self.is_empty(new_x, new_y):
            return False
        
        # cear old position
        self.grid[agent.y][agent.x] = None
        
        #new position
        self.grid[new_y][new_x] = agent
        agent.x = new_x
        agent.y = new_y
        
        return True


if __name__ == "__main__":
    print("Testing Grid class...")
    
   
    grid = Grid(10, 10)  # Smaller for testing
    print(f"Created {grid.width}x{grid.height} grid")
    
    
    print("\nEmpty grid:")
    grid.display()
    
    # wrapping
    print("Testing position wrapping:")
    test_cases = [
        (0, 0, "Normal position"),
        (10, 5, "Right edge wrap"),
        (-1, 5, "Left edge wrap"),
        (5, 10, "Bottom edge wrap"),
        (5, -1, "Top edge wrap"),
        (-2, -3, "Both negative"),
    ]
    
    for x, y, description in test_cases:
        norm_x, norm_y = grid.normalize_position(x, y)
        print(f"  {description:20s}: ({x:3d}, {y:3d}) -> ({norm_x:2d}, {norm_y:2d})")
    

    print("\nTesting position validation:")
    print(f"  (5, 5) valid? {grid.is_valid_position(5, 5)}")    # True
    print(f"  (10, 5) valid? {grid.is_valid_position(10, 5)}")  # False (out of bounds)
    print(f"  (-1, 5) valid? {grid.is_valid_position(-1, 5)}")  # False
    
    print("\nGrid tests complete!")