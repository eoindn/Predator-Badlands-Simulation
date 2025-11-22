import sys
import random
sys.path.append('src')


from core.grid import Grid
from entities.synthetics import Synthetic
from entities.monster import Monster
from entities.predator import Predator

# Now test here
grid = Grid(10, 10)



thia = Synthetic(5, 5, "Thia",True)
monster = Monster(6,6,"Thylacoleo")
dek = Predator(5,7,"Dek",True)



grid.place_agent(thia, 5, 5)
grid.place_agent(monster, 6, 6)
grid.place_agent(dek, 5, 7)

for i in range(10):
    x,y = thia.get_pos()
    new_x = x + i
    new_y = y + i
    grid.move_agent(thia,new_x,new_y)
    grid.display()




print("Testing scan...")
results = thia.scan_area(grid, scan_range=3)

print(f"Monsters: {results['monsters']}")
print(f"Predators: {results['predators']}")
print(f"Synthetics: {results['synthetics']}")