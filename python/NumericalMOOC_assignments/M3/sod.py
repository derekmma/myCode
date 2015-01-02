import numpy
from numpy import repeat

nx = 81
dx = 0.25
dt = 0.0002
gamma = 1.4
T = 0.01

nt = int(T/dt)+1

def rhoET(u):
    rho = u[0]
    v = u[1]
    p = u[2]*1000
    return p/((gamma-1)) + .5*v**2*rho

def fluxVector(u):
    u1 = u[0,]
    u2 = u[1,]
    u3 = u[2,]
    p = numpy.zeros((3,len(u1)))
    p[:,:] = [u2,(u2**2/u1)+(gamma-1)*(u3-0.5*u2**2/u1),(u2/u1)*(u3+(gamma-1)*(u3 - 0.5*u2**2/u1))]
    return p

def richtmeyer(u):
    fPred = fluxVector(u)
    uPred = 0.5*(u[:,1:]+u[:,:-1])-0.5*dt/dx*(fPred[:,1:]-fPred[:,:-1])
    fCor = fluxVector(uPred)
    uCor = u[:,1:-1] - dt/dx*(fCor[:,1:] - fCor[:,:-1])
    return uCor

ICL = numpy.array([1.,0.,100.])
ICR = numpy.array([0.125,0.,10.])

u = numpy.zeros((nt,3,nx))

u[0,:,:] = [repeat(ICR[0],nx),repeat(0.,nx),repeat(rhoET(ICR),nx)]
u[0,:,:40] = [repeat(ICL[0],40),repeat(0.,40),repeat(rhoET(ICL),40)]


for n in range (1,nt):
    u[n] = u[n-1].copy()
    u[n,:,1:-1] = richtmeyer(u[n-1])

u1 = u[nt-1,0]
u2 = u[nt-1,1]
u3 = u[nt-1,2]

from matplotlib import pyplot
p = (gamma-1)*(u3 - 0.5*u2**2/u1)
u = u2/u1
rho = u1
x = numpy.linspace(-10,10,nx)

print "The parameters at x = 2.5 m are:\n"
print "1. Pressure = " , p[50] , "$N/m^2$\n"
print "2. Velocity = " , u[50] , "$m/s^2$\n"
print "3. Density = " , rho[50] , "$kg/m^3$\n"

fig = pyplot.figure()
ax1 = fig.add_subplot(1,3,1)
ax1.plot(x,p,'k-')
ax1.set_title('Pressure($N/m^2$)')
ax2 = fig.add_subplot(1,3,2)
ax2.plot(x,u,'k-')
ax2.set_title('Velocity($m/s^2$)')
ax3 = fig.add_subplot(1,3,3)
ax3.plot(x,rho,'k-')
ax3.set_title('Density($kg/m^3$)')
pyplot.show()
