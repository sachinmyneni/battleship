from microbit import *
import radio
import random
import speech
import music

class Ship:
    len = 0
    def __init__(self,leds):
        self.leds = leds

    def __repr__(self):
        return ("{}:{}".format(self.__class__.__name__,self.leds))
        
    def get_status(self):
        one = self.leds.pop()
        return display.get_pixel(one[0],one[1])

    def set_status(self):
        if self.get_status() == 9: # full life
            new = 4
        if self.get_status() == 4: # 1 hit
            new = 0
        else:                      # sink
            new = 0
        self.set_levels(new)

    def set_levels(self,new):
        for led in self.leds:
            display.set_pixel(led[0],led[1],new)

class Battleship(Ship):
    len = 3
class Frigate(Ship):
    len = 2
class Dingy(Ship):
    len = 1
    
class Board:
    def __init__(self):
        """ Initialize a board with 3 vessles.
        1 dingy (length=1)
        2 frigate (length=2)
        3 battleship (length=3)
        """
        random.seed(int(temperature()))
        # random.seed(42)
        # initialize battleship
        x = random.randrange(3)
        y = random.randrange(3)
        hv = random.choice([0,1])
        if hv == 0: #horizontal
            self.btlshp = {(x,y),(x+1,y),(x+2,y)}
        else:
            self.btlshp = {(x,y),(x,y+1),(x,y+2)}

        b = Battleship(self.btlshp)

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

        f = Frigate(self.frgt)
        
        while True:
            g = random.randint(0,4)
            h = random.randint(0,4)
            self.dingy = {(g,h)}
            if self.btlshp.isdisjoint(self.dingy) and self.frgt.isdisjoint(self.dingy):
                break
            else:
                ...
        d = Dingy(self.dingy)
        
        print("{}".format(b))
        print("{}".format(f))
        print("{}".format(d))
        
    def show_board(self):
        display.clear()
        for ship in (self.btlshp,self.dingy,self.frgt):
            for coord in ship:
                display.set_pixel(coord[0],coord[1],9)

    def get_ship_status(self, v:Ship):
        # return the current status (get_pixel?) of the ship
        # under question.
        ...
    def hit_or_miss(self,x:int,y:int) -> int:
        """ Given target x,y 
        return 0 for no hit
        1 for dingy
        2 for frigate
        3 for battleship """
        if {(x,y)}.isdisjoint(self.btlshp) and \
           {(x,y)}.isdisjoint(self.frgt) and \
           {(x,y)}.isdisjoint((self.dingy)):
            return 0
        if not {(x,y)}.isdisjoint(self.btlshp):
            return 3
        if not {(x,y)}.isdisjoint(self.frgt):
            return 2
        if not {(x,y)}.isdisjoint((self.dingy)):
            return 1
        else:
            raise ValueError("Not a miss and not a hit either at {},{}".format(x,y))
        
        
    def get_board(self)->tuple:
        return (self.btlshp,self.frgt,self.dingy)

    def sink(self,s:int):
        """ If the ship is hit once, delete the variable?
        There can be better ways of doing this... like dimming
        the leds associated with this sunken ship."""
        if s == 3:
            del self.btlshp
        if s == 2:
            del self.frgt
        if s == 1:
            del self.dingy

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
            else:
                x = x % 4
            print("X,y={},{}".format(x,y))
            display.set_pixel(x,y,9)
    
        if button_b.is_pressed():
            display.clear()
            print("x,Y={},{}".format(x,y))
            if y < 4 :
                y = y + 1
            else:
                y = y % 4
            display.set_pixel(x,y,9)
            
        if button_a.is_pressed() and button_b.is_pressed():
            return x,y
 
    
def fire(x:int,y:int):
    # Send location of the target to 
    # the other microbit
    radio.send(str(x)+","+str(y))

def main():
    # Set board
    my_turn = True
    b = Board()
    formation = b.get_board()
    print("Formation: {}".format(formation))
    radio.config(group=23)
    radio.on()
    # Choose whose turn it is
    while True:
        mine = "True" if random.choice((True,False)) else "False"
        radio.send(mine)
        theirs = radio.receive()
        if theirs != mine and theirs != "begin":
            my_turn = True if mine == "True" else False
            radio.send("begin")
            break
        if theirs == mine and theirs != "begin":
            continue
        if theirs == "begin":
            radio.send("begin")
            break
        sleep(100)

    # Fight!
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
                # show_my_ships(formation)
                b.show_board()
                while True:
                    target = radio.receive()
                    if target in ["True","False","begin"]:
                        continue
                    if type(target) is str:
                        display.scroll("target={}".format(target))
                        display.scroll("type={}".format(type(target)))
                        x,y = target.split(",")
                        display.set_pixel(int(x),int(y),4)
                        yn = b.hit_or_miss(int(x),int(y))
                        if yn == 0:
                            music.play(music.WAWAWAWAA)
                        if yn == 1:
                            speech.say("You sank my dingy")
                        if yn == 2:
                            speech.say("You sank my frigate")
                        if yn == 3:
                            speech.say("You sank my battleship")
                        my_turn = True
                        break
                    sleep(100)
                my_turn = True

        
if __name__ == "__main__":

    main()
