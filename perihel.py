'''
                          Die relativistische Periheldrehung
                           Copyright (c) 2021 Franz Scheerer 
                                Alle Rechte vorbehalten 
                                 all rights reserved
'''
import math

print("Die Periheldrehung eines schnellen Planeten")
e = 0.1
vy = 1.0*(1.0+e)
vx = 0.0
#
# Die Geschwindigkeit des Planeten sei 
# etwa ein Prozent der Lichtgeschwindigkeit
#
c = 100.0
#
# Der Lorentzfaktor gamma (1 - (v/c)^2) ^ {-1/2}
#
gamma = 1.0 / math.sqrt(1.0 - (vx*vx + vy*vy)/(c*c))
#
# Die Ruhemasse sei 1 
# ==> relativitische Masse gleich gamma
#
px = vx * gamma
py = vy * gamma

x = (-1)*(1.0-e)
y = 0.0

t = 0.0
dt = 0.00001

s0 = px*x + py*y
y0 = y
t0 = t
while t < 30:
    t += dt      
    gamma = 1.0 / math.sqrt(1.0 - (vx*vx + vy*vy)/(c*c))
    r = math.sqrt(x*x + y*y)
    r3 = r * r * r
    px -= gamma*(x/r3)*dt
    py -= gamma*(y/r3)*dt
    vx = px / gamma
    vy = py / gamma
    x += vx * dt 
    y += vy * dt
    omega = math.sqrt(vx*vx + vy*vy) / r
    #
    # Vorzeichenwechsel bedeutet Planet in ursprünglicher Lage des Perihels oder Aphels
    #
    if y0*y < 0.0:
       print("y = 0 ", t)
       print("r = 0 ", math.sqrt(x*x + y*y))
       t0 = t
    #
    # Vorzeichenwechsel bedeutet Planet in Apohel oder Perihel
    #
    if s0*(px*x + py*y) < 0.0:
       print("s = 0 ", t , "relative Drehung ", omega * (t - t0)/t)
    s0 = px*x + py*y
    y0 = y



