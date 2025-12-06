from entities.agent import Agent


class Trap(Agent):

    def __init__(self,x,y,symbol,name = "Trap"):

        super().__init__(x,y,symbol,name)

        self.is_triggered = False
        self.x = x
        self.y = y
        self.symbol = symbol
        self.name = name
        

    def get_pos(self):
        return (self.x,self.y)
    


    def damage(self):
        return 20
    

    