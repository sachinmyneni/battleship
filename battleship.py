# Imports go at the top
from microbit import *
import radio
import random

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
            print("X,y={},{}".format(x,y))
            display.set_pixel(x,y,9)
    
        if button_b.is_pressed():
            display.clear()
            print("x,Y={},{}".format(x,y))
            if y < 4 :
                y = y + 1
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
    formation = init_formation()
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
                        x,y = target.split(",")
                        display.set_pixel(int(x),int(y),4)
                        break
                    sleep(100)
                my_turn = True
        
        
if __name__ == "__main__":
    main()
