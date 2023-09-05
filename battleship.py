# Imports go at the top
from microbit import *
import radio
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
            self.btlshp = {(x,y),(x+1,y),(x+2,y)}
        else:
            self.btlshp = {(x,y),(x,y+1),(x,y+2)}

        # initialize frigate
        while True:
            p = random.randrange(4)
            q = random.randrange(4)
            hv = random.choice([0,1])
            if hv == 0:
                self.frgt = {(p,q),(p+1,q)}
            else:
                self.frgt = {(p,q),(p,q+1)}

            if self.btlshp.isdisjoint(self.frgt):
                break
            else:
                ...

        while True:
            g = random.randint(0,4)
            h = random.randint(0,4)
            self.dingy = {(g,h)}
            if self.btlshp.isdisjoint(self.dingy) and self.frgt.isdisjoint(self.dingy):
                break
            else:
                ...

        print("Battleship: {}".format(self.btlshp))
        print("Frigate:    {}".format(self.frgt))
        print("Dingy:      {}".format(self.dingy))
        
        self.ships = '00900:00900:00900:00000:99009'
        display.show(Image(self.ships))

    def hit_or_miss(self,x:int,y:int) -> int:
        """ Given target x,y 
        return 0 for no hit
        1 for dingy
        2 for frigate
        3 for battleship """
        if {(x,y)}.isdisjoint(self.btlshp) and {(x,y)}.isdisjoint(self.frgt) and {(x,y)}.isdisjoint((self.dingy)):
            return 0
        if not {(x,y)}.isdisjoint(self.btlshp):
            return 3
        if not {(x,y)}.isdisjoint(self.frgt):
            return 2
        if not {(x,y)}.isdisjoint((self.dingy)):
            return 1
        else:
            raise ValueError("Not a miss and not a hit either at {},{}".format(x,y))
        
        
    def get_board(self):
        return self.ships

def set_ships():
    ...

def init_formation():
    # Create a formation of ships 
    # either randomly or manually
    return '00900:00900:00900:00000:99009'

def my_target():
    # a blinking led that can be moved
    # with 1 button. Select with another 
    # button
    x = 0
    y = 0
    display.set_pixel(x,y,9)
    while True:
        sleep(100)
        if button_a.is_pressed():
            display.clear()
            if x < 4 :
                x = x + 1
            if x > 4:
                x = x % 4
            print("X,y={},{}".format(x,y))
            display.set_pixel(x,y,9)
    
        if button_b.is_pressed():
            display.clear()
            print("x,Y={},{}".format(x,y))
            if y < 4 :
                y = y + 1
            if y > 4:
                y = y % 4
            display.set_pixel(x,y,9)
            
        if button_a.is_pressed() and button_b.is_pressed():
            return x,y
 
    
def fire(x:int,y:int):
    # Send location of the target to 
    # the other microbit
    radio.send(str(x)+","+str(y))

def show_my_ships(form:str):
    display.show(Image(form))    


def main():
    my_turn = True
    b = Board()
    formation = b.get_board()
    radio.config(group=23)
    radio.on()
    while True:
        mine = random.choice((True,False))
        radio.send("True" if mine else "False")
        theirs = radio.receive()
        if theirs != mine and theirs != "begin":
            my_turn = True if mine else False
            radio.send("begin")
            break
        if theirs == "begin":
            sleep(200)
            break
        sleep(100)
    while True:
        while True:
            if my_turn:
                x,y = my_target()
                print("targetting {}{}".format(x,y))
                print("firing @ {}{}".format(x,y))
                fire(x,y)
                my_turn = False
                break
            else:
                show_my_ships(formation)
                while True:
                    target = radio.receive()
                    if type(target) is str:
                        # display.scroll("target={}".format(target))
                        # display.scroll("type={}".format(type(target)))
                        x,y = target.split(",")
                        display.set_pixel(int(x),int(y),4)
                        break
                    sleep(100)
                my_turn = True
        
        
if __name__ == "__main__":
    main()
