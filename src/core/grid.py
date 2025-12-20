import random

class Grid:
    """
    2D grid environment representing Kalisk.
    Each cell can hold one agent or be empty,
   
    """

    def __init__(self, width=20, height=20):
        self.width = width
        self.height = height
        # Initialise a 2D list where each cell is initially None (empty)
        self.grid = [[None for _ in range(width)] for _ in range(height)]

    def normalise_position(self, x, y):
        """
        Wrap coordinates around the grid
        """
        return x % self.width, y % self.height

    def is_valid_position(self, x, y):
        """
        Check if a position is within the actual grid boundaries (without wrapping).
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def display(self):
        """ Displays the grid, obviosusly """
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
        x, y = self.normalise_position(x, y)
        return self.grid[y][x] is None

    def get_cell(self, x, y):
        
        x, y = self.normalise_position(x, y)
        return self.grid[y][x]

    def place_agent(self, agent, x, y):
        """
        Attempt to place an agent at a normalised position.
        Returns False if the spot is occupied.
        """
        x, y = self.normalise_position(x, y)

        if not self.is_empty(x, y):
            return False

        self.grid[y][x] = agent
        # Update agent's internal position tracking
        agent.x = x
        agent.y = y
        return True

    def remove_agent(self, agent):
        """
        Remove an agent from its current position on the grid.
        This method relies on the agent's stored position being correct.
        """
        # A quick bounds check before attempting removal
        if self.is_valid_position(agent.x, agent.y):
            self.grid[agent.y][agent.x] = None



    def weather_system(self):
        """
        Returns a random weather string.
        """
        weather_options = {
            1: "hot",
            2: "cold",
            3: "rainy",
            4: "thunder_storm"
        }
        return random.choice(list(weather_options.values()))

    def move_agent(self, agent, new_x, new_y):
        new_x, new_y = self.normalise_position(new_x, new_y)

        #see if the new spot is available
        if not self.is_empty(new_x, new_y):
            return False

        # Clear the agent old position
        self.grid[agent.y][agent.x] = None

        #place the agent in the new position and update its coordinates
        self.grid[new_y][new_x] = agent
        agent.x = new_x
        agent.y = new_y

        return True

if __name__ == "__main__":
    print("Initiating Grid class demonstration...")

    grid = Grid(10, 10)  #samller grid for testing
    print(f"Created a new {grid.width}x{grid.height} grid instance.")

    print("\nDisplaying the initial empty grid:")
    grid.display()
        # Testing the wrapping logic
    # print("Verifying position wrapping using normalise_position():")
    # test_cases = [
    #     (0, 0, "Normal position"),
    #     (10, 5, "Right edge wrap"),
    #     (-1, 5, "Left edge wrap"),
    #     (5, 10, "Bottom edge wrap"),
    #     (5, -1, "Top edge wrap"),
    #     (-2, -3, "Both negative"),
    # ]

    # for x, y, description in test_cases:
    #     norm_x, norm_y = grid.normalise_position(x, y)
    #     print(f"  {description:20s}: ({x:3d}, {y:3d}) -> ({norm_x:2d}, {norm_y:2d})")

    # Testing the validation logic
    # print("\nVerifying position validity within bounds using is_valid_position():")
    # print(f"  (5, 5) valid? {grid.is_valid_position(5, 5)}")    # Expected: True
    # print(f"  (10, 5) valid? {grid.is_valid_position(10, 5)}")  # Expected: False (out of bounds)
    # print(f"  (-1, 5) valid? {grid.is_valid_position(-1, 5)}")  # Expected: False

    # print("\nGrid class tests concluded successfully.")
