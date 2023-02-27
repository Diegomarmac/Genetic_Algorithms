import turtle
import inspect
import random
import pickle
from argparse import ArgumentParser

def draw_bag():
    turtle.shape("turtle")
    turtle.pen(pencolor="brown", pensize=5)
    turtle.penup()
    turtle.goto(-35,35)
    turtle.pendown()
    turtle.right(90)
    turtle.forward(70)
    turtle.left(90)
    turtle.forward(70)
    turtle.left(90)
    turtle.forward(70)

def scaped(position): # wiht this we can know when the turtle has scaped
    x = int(position[0])
    y = int(position[1])
    return x < -35 or x > 35 or y < -35 or y > 35

def draw_line(): #Scape in a simple way, just a line
    angle = 0
    step = 5
    t = turtle.Turtle()
    while not scaped(t.position()):
        t.left(angle)
        t.forward(step)

    #Scape using squares
def draw_square(t,size):
    L = []
    for i in range(4):
        t.forward(size)
        t.left(90)
        store_position_data(L,t)
    return L

def store_position_data(L,t):
    position = t.position()
    L.append([position[0], position[1], scaped(position)])

def draw_squares(number):
    t = turtle.Turtle()
    L = []
    for i in range(1, number + 1):
        t.penup()
        t.goto(-i, -i)
        t.pendown()
        L.extend(draw_square(t,i*2))
    return L

def draw_squares_until_scaped(n):
    t = turtle.Turtle()
    L = draw_squares(n)
    with open("data_square", "wb") as f:
        pickle.dump(L, f)

## We can make triangles, go 120 degrees three times ;)
def draw_triangles(number):
    t = turtle.Turtle()
    for i in range(1,number):
        t.forward(i*10)
        t.right(120)
# we can also try something random
def draw_spirals_until_scaped():
    t = turtle.Turtle()
    t.penup()
    t.left(random.randint(0,360))
    t.pendown()
    
    i = 0
    turn = 360/random.randint(1,10)
    L = []
    store_position_data(L, t)
    while not scaped(t.position()):
        i += 1
        t.forward(i*5)
        t.right(turn)
        store_position_data(L, t)
    return L

def draw_random_spirangles():
    L = []
    for i in range (10):
        L.extend(draw_spirals_until_scaped())
        
    with open("data_rand", "wb") as f:
        pickle.dump(L,f)

if __name__ == '__main__':
    fns = {"line": draw_line,
            "squares": draw_squares_until_scaped,
            "triangles": draw_triangles,
            "spirangles" : draw_random_spirangles
          }
    
    parser = ArgumentParser()
    parser.add_argument("-f", "--function",
                        choices = fns,
                        help= "one of " + ", ".join(fns.keys()))
    parser.add_argument("-n", "--number", default = 50, type=int, help="how many?")
    args = parser.parse_args()
    
    try:
        f = fns[args.function]
        turtle.setworldcoordinates(-70.,-70.,70.,70.)
        draw_bag()
        turtle.hideturtle()
        if len(inspect.getargspec(f).args)==1:
            f(args.number)
        else:
            f()
        turtle.mainloop()
    except KeyError:
        parser.print_help()