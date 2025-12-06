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




print("Clan Dialogue System Test")

#dek with low honour
dek_low = Predator(5, 5, "Dek", isDek=True)
dek_low.honour = 25
dek_low.kills = 0

father = Predator(6, 6, "Father", isDek=False)
brother = Predator(7, 7, "Brother", isDek=False)

print(father.clan_dialogue(dek_low))
print(brother.clan_dialogue(dek_low))

#give Dek high honour
dek_high = Predator(10, 10, "Dek", isDek=True)
dek_high.honour = 75
dek_high.kills = 5

print(f"after Dek proves himself")
print(father.clan_dialogue(dek_high))
print(brother.clan_dialogue(dek_high))