from turtle import *
k=70
left(90)
tracer(0)

for i in range(18):
    forward(4*k)
    left(90)
    forward(7*k)
    left(90)

penup()
forward(3*k)
right(37)
pendown()

for i in range(18):
    forward(7*k)
    right(90)
    forward(4*k)
    right(90)
left(37)
penup()
forward(4*k)
left(168)
pendown()

for i in range(20):
    forward(6*k)
    right(90)
    forward(3*k)
    right(90)
penup()

for x in range(-30, 30):
    for y in range(-30, 30):
        setpos(x*k, y*k)
        dot(3)
update()
done()