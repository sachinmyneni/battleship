# Your new file!
from microbit import *
import random

class Board:
    def __init__(self):
        """ Initialize a board with 3 vessles.
        1 dingy (length=1)
        2 frigate (length=2)
        3 battleship (length=3)
        """
        random.seed(int(temperature()))
        # initialize battleship
        x = random.randrange(3)
        y = random.randrange(3)
        hv = random.choice([0,1])
        if hv == 0: #horizontal
            btlshp = {(x,y),(x+1,y),(x+2,y)}
        else:
            btlshp = {(x,y),(x,y+1),(x,y+2)}

        # initialize frigate
        while True:
            p = random.randrange(4)
            q = random.randrange(4)
            hv = random.choice([0,1])
            if hv == 0:
                frgt = {(p,q),(p+1,q)}
            else:
                frgt = {(p,q),(p,q+1)}

            if btlshp.isdisjoint(frgt):
                break
            else:
                ...

        while True:
            g = random.randint(0,4)
            h = random.randint(0,4)
            dingy = {(g,h)}
            if btlshp.isdisjoint(dingy) and frgt.isdisjoint(dingy):
                break
            else:
                ...

        print("Battleship: {}".format(btlshp))
        print("Frigate: {}".format(frgt))
        print("Dingy: {}".format(dingy))
        
        self.ships = '00900:00900:00900:00000:99009'
        display.show(Image(self.ships))

    def get_vessel(self,x:int,y:int) -> int:
        """ Given target x,y
        return the vessel occupying the 
        coordinates"""
        return 0
        
    def hit_or_miss(self,x:int,y:int) -> int:
        """ Given target x,y 
        return 0 for no hit
        1 for dingy
        2 for frigate
        3 for battleship """
        return 0
        
    def get_board(self):
        return self.ships

def main():
    b = Board()
    print(b.get_board())