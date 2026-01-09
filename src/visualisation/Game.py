import sys
import os
# THIS MUST BE BEFORE THE CORE IMPORT
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from core.simulation import Simulation

class GameVisualizer:
    def __init__(self, sim):
        
        self.sim = sim
        self.cell_size = 20


        self.root = tk.Tk()
        self.root.title("Badlands Visualizer")


        width = self.sim.width * self.cell_size
        height = self.sim.height* self.cell_size
        self.canvas = tk.Canvas(self.root,width=width , height=height)
        self.canvas.pack(side=tk.LEFT)   

        self.stats_text = tk.Text(self.root, width=40, height=30, bg='#1a1a1a', fg='white')
        self.stats_text.pack(side = tk.RIGHT, fill = tk.BOTH)

        control_frame = tk.Frame(self.root)
        control_frame.pack(side = tk.BOTTOM)

        tk.Button(control_frame, text= "Next Turn", command=self.run_turn).pack(side=tk.LEFT)     
        tk.Button(control_frame, text="Run 10 Turns", command=self.run_10).pack(side=tk.LEFT)

        self.auto_running = False
        self.auto_btn = tk.Button(control_frame, text="Auto Run", command = self.toggle_auto)  
        self.auto_btn.pack(side=tk.LEFT)

        self.colors = {
            'D': '#00ff00',
            'P': '#00aaff',
            'M': '#ff0000',
            'X': '#ff00ff',
            'T': "#8a8a1c",
            'H': '#ff8800',
            'R': '#888888',
            'S': '#00ffff',
            'W': '#ffffff',
        }
        self.draw_grid()
        self.update_stats()

    def draw_grid(self):
        self.canvas.delete("all")

        for i in range(self.sim.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x,0,x,self.sim.height * self.cell_size, fill='grey')

        for i in range(self.sim.height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0,y,self.sim.width * self.cell_size,y, fill='grey')

        for y in range(self.sim.height):
            for x in range(self.sim.width):
                entity = self.sim.grid.get_cell(x,y)
                if hasattr(entity, 'symbol'):
                    self.draw_entity(x,y,entity.symbol)

    def draw_entity(self, x, y, entity_symbol):
        x1 = x * self.cell_size + 2
        y1 = y * self.cell_size + 2
        x2 = x1 + self.cell_size - 4
        y2 = y1 + self.cell_size - 4

        color = self.colors.get(entity_symbol, '#000000')
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)

        cx = x * self.cell_size + self.cell_size // 2
        cy = y * self.cell_size + self.cell_size // 2
        self

        text_color = 'black' if entity_symbol is ['D', 'T', 'S', 'W'] else 'white'
        self.canvas.create_text(cx, cy, text=entity_symbol, fill=text_color, font=('Arial', 14, 'bold'))

    def update_stats(self):
        self.stats_text.delete(1.0, tk.END)

        stats = f"""

TURN: {self.sim.turn}
Wather = {self.sim.current_weather}


Predatorts:
"""
        for pred in self.sim.predators:
            if pred.alive:
                stats += f" Predator {pred.name}: \n"
                stats += f" Health {pred.health} \n"
                stats += f" Stamina {pred.stamina} \n"
                stats += f" Honor {pred.honor} \n"


        stats += f"Monster Alive: {len([m for m in self.sim.monsters if m.alive])} \n"
        stats += f"Sythetics Alive: {len([s for s in self.sim.synthetics if s.alive])} \n"  



        stats += f"\nSTATS:\n"
        stats += f"  Combats: {self.sim.stats['combats']}\n"
        stats += f"  Kills: {self.sim.stats['kills']}\n"
        stats += f"  Deaths: {self.sim.stats['deaths']}\n"
        stats += f"  Resources: {self.sim.stats['resources_collected']}\n"


        self.stats_text.insert(1.0, stats)
        
    def run_turn(self):

        if self.sim.turn >= self.sim.max_turns:
            return
        

        self.sim.turn += 1
        self.sim.stats['turns'] = self.sim.turn

        self.sim._update_agents()
        self.sim.weather_update()
        
        self.draw_grid()
        self.update_stats()
        
        if self.sim._check_win_conditions():
            self.auto_running = False
    
    def run_10(self):
        for _ in range(10):
            self.run_turn()
            if not any(m.alive for m in self.sim.monsters):
                break
    
    def toggle_auto(self):
        self.auto_running = not self.auto_running
        self.auto_btn.config(text="Stop" if self.auto_running else "Auto Play")
        if self.auto_running:
            self.auto_play()
    
    def auto_play(self):
        if self.auto_running and self.sim.turn < self.sim.max_turns:
            self.run_turn()
            self.root.after(500, self.auto_play)
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    sim = Simulation(width=20, height=20, num_predators=3, num_monsters=5, num_synthetics=2)
    visualizer = GameVisualizer(sim)
    visualizer.run()


