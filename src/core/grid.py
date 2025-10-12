class Grid:
    """
    2D grid environment representing planet Kalisk.
    
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
       
        return x % self.width, y % self.height
    
    def is_valid_position(self, x, y):
       
        return 0 <= x < self.width and 0 <= y < self.height
    
    def display(self):
        """
        Print grid to console.

        
        Symbols (planned):
            . = empty
            D = Dek (Predator)
            M = Monster
            T = Thia (Synthetic)
            P = Other Predator
            X = Ultimate Adversary
        """
        print("\n" + "=" * (self.width * 2 + 1))
        for row in self.grid:
            line = ""
            for cell in row:
                if cell is None:
                    line += ". "
                else:
                    # Once agents are added this will show theirr symbol
                    line += "? "
            print(line)
        print("=" * (self.width * 2 + 1) + "\n")



if __name__ == "__main__":
    print("Testing Grid class...")
    
    
    grid = Grid(10, 10)  # Smaller for testing
    print(f"Created {grid.width}x{grid.height} grid")
    
    # Test display
    print("\nEmpty grid:")
    grid.display()
    

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
    
    # Test validation
    print("\nTesting position validation:")
    print(f"  (5, 5) valid? {grid.is_valid_position(5, 5)}")    # True
    print(f"  (10, 5) valid? {grid.is_valid_position(10, 5)}")  # False (out of bounds)
    print(f"  (-1, 5) valid? {grid.is_valid_position(-1, 5)}")  # False
    
    print("\nGrid tests complete!")