#############################################################################
#                                                                           #
#                         TRAFFIC MODEL - PART B                            #
#                                                                           #
#############################################################################

# Definitions:
#
# V = speen of Traffic in kmph.
# rho = traffic density in cars/km
# F = traffic flux/ flow rate of cars in cars per hour.

# Assumptions:

# If there are very few cars on the road, the cars drive fast at Vmax.
# If cars are bumper to bumper,
# V approaches zero and rho approaches rhoMax.
# 
# Equations:
#
# V = Vmax * ( 1 - rho/rhoMax)
# and F = V*rho

#PDEs:

# dabba(rho)/dabba(t) + dabba(F)/dabba(x) = 0


# Discretization scheme: Forward Time Backward Space.

# Physical Conditions:

# 1. Stretch of road, L = 11 km 
# 2. Vmax = 136 kmph
# 3. rhoMax = 250 cars/km 
# 4. grid points for spatial parameter x, nx = 51
# 5. time step size, dt = 0.001 hours 

import numpy

L = 11.
Vmax = 136.
rhoMax = 250.
nx = 51
dt = 0.001
dx = L/(nx-1)           # Step Size for Spatial Parameter

# Time and Space Discretization

T = 3./60
N = int(T/dt) + 1         # No. of grid points for time domain

# Initial Conditions:

x = numpy.linspace(0,L,nx)
rho0 = numpy.ones(nx)*20.
rho0[10:20] = 50.

# Question 1:

# Defining "F" using Sympy

from sympy import symbols,utilities,lambdify

rho = symbols('rho')
fValue = lambdify(rho,Vmax*rho*(1-rho/rhoMax))

# F value at t = 0 minutes:

F0 = numpy.empty_like(rho0)
F0[0:]=fValue(rho0[0:])

minVal0 = max(F0)/max(rho0)*5./18
print "\n The Minimum Speed at time T=0 minutes is ",format(minVal0,"0.2f"),"\n"

#  Question 2:

for n in range(1,N):
    rhoCopy = rho0.copy()
    rho0[1:] = rhoCopy[1:]+dt/dx*(F0[:50]-F0[1:])
    F0[0:]=fValue(rho0[0:])

# Defining V using SymPy:

vel = lambdify(rho,Vmax*(1-rho/rhoMax))
V = numpy.empty_like(rho0)
V[0:] = vel(rho0[0:])

print "\n The average Velocity at Time T = 3 min is ", format((sum(V)/51*5./18),"0.2f"),"\n"

#  Question 3:

minVal0 = max(F0)/max(rho0)*5./18
print "\n The Minimum Speed at time T=3 minutes is ",format(minVal0,"0.2f"),"\n"
