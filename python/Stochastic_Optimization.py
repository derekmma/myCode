from numpy.random import uniform
from math import exp
from operator import itemgetter

def metropolisMC(f, nIter, nVar, upper, lower):
    """
    Description: Finds the Minimum of a function using the Metropolis Monte-Carlo method for accepting non-improving moves.

    Inputs :
 
           f     : Function to be minimized
           nIter : Number of Global iterations to perform the search over
           nVar  : Number of variables involved in function f
           upper : Upper search limit
           lower : Lower search limit

    Outputs:
            
            Returns a list with 2 elements
             i) fist element   : The minimum value of f
            ii) second element : List of coordinates corresponding to the minimum
   
    Note: Values are obtained after max(100 x nIter) search attempts. 
           
    """
    bestVal = [] ; bestCoord = []
    for n in range(nIter):
        for i in range(100):
            if i == 0 :
                step = [float(uniform(lower,upper,1)) for m in range(nVar)]; min_Coord = [m for m in step]
                minVal = E = f(min_Coord)
            else:
                if any(m > upper or m < lower for m in step ):break
                step = [m + float(uniform(-1,1,1)) for m in step] ; E_new = f(step)
                deltaE = E_new - E
                if deltaE < 0 : minVal = E = E_new ; min_Coord = [m for m in step]
                elif float(uniform(0,1,1)) < exp(-deltaE) : minVal = E = E_new ; min_Coord = [m for m in step]
        bestVal.append(minVal); bestCoord.append(min_Coord)
    index = min(enumerate(bestVal),key = itemgetter(1))[0]
    return [bestVal[index],bestCoord[index]]

def SimpleMC(f, nIter, nVar, upper, lower):
    """
    Description: Finds the Minimum of a function using the Simple Monte-Carlo method (all non-improving moves are discarded)

    Inputs :
 
           f     : Function to be minimized
           nIter : Number of Global iterations to perform the search over
           nVar  : Number of variables involved in function f
           upper : Upper search limit
           lower : Lower search limit

    Outputs:
            
            Returns a list with 2 elements
             i) fist element   : The minimum value of f
            ii) second element : List of coordinates corresponding to the minimum
   
    Note: Values are obtained after max(100 x nIter) search attempts. 
           
    """
    bestVal = [] ; bestCoord = []
    for n in range(nIter):
        for i in range(100):
            if i == 0 :
                step = [float(uniform(lower,upper,1)) for m in range(nVar)]; min_Coord = [m for m in step]
                minVal = E = f(min_Coord)
            else:
                if any(m > upper or m < lower for m in step ):break
                step = [m + float(uniform(-1,1,1)) for m in step] ; E_new = f(step)
                deltaE = E_new - E
                if deltaE < 0 : minVal = E = E_new ; min_Coord = [m for m in step]
        bestVal.append(minVal); bestCoord.append(min_Coord)
    index = min(enumerate(bestVal),key = itemgetter(1))[0]
    return [bestVal[index],bestCoord[index]]


