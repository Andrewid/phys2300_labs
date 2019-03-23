"""
The purpose of this python script is to produce a table using vPython
Copywright Andrew Quinn Merrell
Written for PHYS 2300 Spring 2019
"""
from vpython import box, cylinder, vector, color
# one plus the square root of five divided by two is approximately Phi
phi = (1 + 5 ** 0.5) / 2 # or quad(1, -1, -1)
tableLength = 10
tableHeight = phi - 1
tableWidth = tableLength * phi
legRadius = tableHeight / 2

table_top = box(size=vector(tableLength, tableHeight, tableWidth))
# move table top up a bit so the legs come out from the bottom
table_top.pos.y = tableHeight / 2
table_top.color = color.green

# make a list of four cylinders for the legs
legs = [cylinder(), cylinder(), cylinder(), cylinder()]

x = 1
z = 1

for leg in legs:
    # Always flip z
    z = z * -1
    # only flip x if z is negative
    # this will only be true half the time
    if z < 0:
        x = x * -1

    # In true binary fashion flipping one every time and the next dependant on the value of the first, we get this pattern
    # z = -1, x = -1
    # z =  1, x = -1
    # z = -1, x =  1
    # z =  1, x =  1

    leg.pos.x = (tableLength - tableHeight) / 2 * x
    leg.pos.z = (tableWidth  - tableHeight) / 2 * z

    leg.axis = vector(0, tableLength - tableWidth, 0)
    leg.radius = legRadius
    # Finally, give the legs some variety
    leg.color = vector(x/2 + .5, .5, z/2 + .5 )
