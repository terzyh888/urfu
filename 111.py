from turtle import *
k=15
left(90)
tracer(0)

for i in range(101):
    forward(10*k)
    left(90)
    forward(4*k)
penup()
forward(5*k)
right(90)
pendown()
for i in range(201):
    backward(12*k)
    right(90)
for i in range(301):
    forward(11*k)
    left(90)
    forward(4*k)
penup()
for x in range(-20, 20):
    for y in range(-20, 20):
        setpos(x*k, y*k)
        dot(3)
update()
done()
