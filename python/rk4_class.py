import numpy
class RK4:

    def __RK4_step(self,dt,x,f):
        k1 = dt * f(x)
        k2 = dt * f(x+k1/2.)
        k3 = dt * f(x+k2/2.)
        k4 = dt * f(x+k3)
        return x + 1./6.*(k1 + 2.*k2 + 2.*k3 + k4)

    def RK4(self,function,start_time,end_time,time_step,init_value):
        """
        Numerical Integration using the Runge-Kutta Fourth Order Method.
        
        Inputs:
                 function : The integrand
               start_time : The lower limit of integration
                 end_time : The upper limit of integration 
                time_step : Discretization step size
               init_value : numpy.ndarray of initial variable values at start_time
        
        Output:
               A numpy.ndarray of discretized  integral values at each grid point
        """
        nGridPoints = int(end_time/time_step) + 1
        time = numpy.linspace(start_time,end_time,nGridPoints)
        x = numpy.zeros((nGridPoints,len([n for n in init_value])))
        x[0] = init_value
        for n in range(nGridPoints-1): x[n+1] = self.__RK4_step(time_step,x[n],function)
        return x
