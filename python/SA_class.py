from numpy import ndarray,zeros_like,exp
from numpy.random import uniform
from rk4_class import RK4

class CoolingSchedule():
    def __init__(self,zeta = None,delta = None):
        self._zeta = zeta
        self._delta = delta

    def _exp(self,temp): return self._zeta * temp
    def _avl(self,temp): pass

class SimulatedAnnealing(RK4,CoolingSchedule):

    def _initial_temp(self): pass 
    # The Optimal Initial Temperature functionality has not been implemented yet.

    def _calculate_energy(self,energy_function,function,init_value,n_unknowns,start_time,end_time,time_step):
        finalValue = self.RK4(function,start_time,end_time,time_step,init_value)[-1][- n_unknowns]
        return energy_function(finalValue)

    def simulated_annealing(self, energy_function, function, start_time, end_time,
                            time_step, temp, init_val, sol_range, cooling_schedule="exp",
                            cooling_parameter = None, acceptance_criteria = None,
                            neighborhood_step = None,room_temp = None, minIter = None,
                            maxIter = None, epsilon = None):
        """
        Parameters
        ----------

        energy_function : callable
            Computes the energy of the system being optimized

        function : callable
            The Definition of the system of differential equations

        start_time : float
            The start time for the Runge-Kutta 4th order method
        
        end_time: float
            End time for the Runge-Kutta 4th order method

        time_step : float
            Time step for the Runge-Kutta 4th order method

        temp : float
            Initial Temperature.

        init_value : list of floats
            Each value corresponds to the known intial values of the problem

        sol_range : list of lists
            Each list corresponds to the search range of the unknown initial value of the problem
        
        cooling_schedule : string (Default = "exp")
            Cooling schedule algorithm to update temperature. 
            Currently supported schedules:  (i) Exponential ("exp")
                                                (ii) Arst and Van Laarhoven ("avl")
        cooling_parameter: float
            Parameter for 
                          (i) Exponential Cooling Schedule (zeta)
                         (ii) Arst and Van Laarhoven Cooling Schedule (delta)
            
            zeta : float (Default = 0.999)
            Parameter for exponential cooling schedule.
            Note : zeta will assume default value if specified value
                   is not between the range ( 0 , 1 )
            
            delta : float (Default = 0.9)
            Parameter for Arst and Van Laarhoven's cooling schedule.
            Note : delta will assume default value if specified value
                   is less than or equal to 0

        acceptance_citeria : string (Default = "metropolis")
            Acceptance criterion for non improving moves.
            Currently supported methods :  (i) Metropolis ("metropolis")
                                          (ii) Glauberg   ("glauberg")

        neighborhood_step : float (Default = 0.01)
            Size of step in the neighborhood of current solution

        room_temp : float (Default = 10.0)
            Temperature at which thermal equilibrium is achieved

        minIter : int (Default = 100)
            Minimum number of steps in the temperature loop

        maxIter :  int (Default = 500)
            Maximum number of steps in the temperature loop

        epsilon : float (Default = 0.01)
            accuracy of the optimization problem

        """

        # Default values of the Parameters
        
        if cooling_schedule not in ["exp","avl"] : raise ValueError("Undefined Cooling Schedule")
        if cooling_schedule is "exp":
            cooling_method = self._exp
            if cooling_parameter <= 0.9 or cooling_parameter >= 1 or cooling_parameter is None : self._zeta = 0.999
            else: self._zeta = cooling_parameter
        else:
            cooling_method = self._avl
            delta = cooling_parameter
            if cooling_parameter <= 0 or cooling_parameter is None: self._delta = 0.9
            else: self._delta = cooling_parameter

        if room_temp is None : room_temp = 10.
        if minIter is None : minIter = 100
        if maxIter is None : maxIter = 500
        if epsilon is None : epsilon = 0.01
        if neighborhood_step is None : neighborhood_step = 0.01

        iterStep = int( 0.2 * (maxIter-minIter) )

        tol_limit = ndarray(len(init_val) + len(sol_range))
        for k in range(len(init_val)): tol_limit[k] = init_val[k]
        for k in range(len(sol_range)): tol_limit[len(init_val) + k] = 1.5 * sol_range[k][1]
       
        while(temp > room_temp):
            if cooling_schedule is "avl" : energy_configurations = []
            for i in range(minIter):
                if i is 0:
                    initVal = zeros_like(tol_limit)
                    for k in range(len(init_val)): initVal[k] = init_val[k]
                    for k in range(len(sol_range)): initVal[len(init_val) + k] = uniform(sol_range[k][0],sol_range[k][1])
                    if not all(tol_limit >= initVal) : break
                    energy = self._calculate_energy(energy_function,function,initVal,len(sol_range),start_time,end_time,time_step)
                else :
                    for k in range(len(sol_range)): initVal[len(init_val) + k] += neighborhood_step * uniform(-1,1) 
                    if not all(tol_limit >= initVal) : break
                    new_energy = self._calculate_energy(energy_function,function,initVal,len(sol_range),start_time,end_time,time_step)
                    delta_energy = new_energy - energy
                    if cooling_schedule is "avl" : energy_configurations.append(delta_energy)
                    if delta_energy < 0 : energy = new_energy
                    elif uniform(0,1) < exp(-delta_energy/temp) : energy = new_energy # Metropolis Acceptance Criteria
                    if energy < epsilon : return [energy,initVal]
                    elif i is minIter and i < maxiter : minIter += iterStep
                    else: temp = cooling_method(temp)
        temp = room_temp
        raise RuntimeError("Stopping Criteria not realized for current parameter settings")
