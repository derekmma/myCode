from sympy import diff,symbols,hessian,poly,matrix2numpy,eye
from numpy import matrix,squeeze,asarray
from numpy.linalg import inv

global epsilon
epsilon = 1E-5

def fValue(f,x0,X):
    """
    Description : Returns the value of the function f evaluated at point x0
    
    
    Parameters:
               1. f   : symbolic representation of the function to be minimized
               2. x0  : list of independant variables for the function
               3. X   : symbolic list of the dependant variables in the function f
    
    Output:
               gradient vector as numpy matrix
    """
    length = range(0,len(x0))
    return f.subs([(X[i],x0[i]) for i in length]) 

def gradValue(gradF,x0,X):
    """
    Description : Returns the value of the gradient of the function evaluated as point x0
    
    Parameters:
               1. gradF : symbolic list of gradient coefficients
               2. x0    : list of independant variables for the function
               3. X     : symbolic list of the dependant variables in the function f
    
    Output:
               gradient vector as numpy matrix
    """
    length = range(0,len(x0))
    gradAsList = [gradF[j].subs( [ (X[i],x0[i]) for i in length] ) for j in length]
    return matrix(gradAsList,'float')

def hessianValue(Q,x0,X):
    """
    Description : Calculates the Value of the Hessian of a function at a specified point
    
    Parameters:
               1. Q   : symbolic representation of the Hessian Matrix
               2. x0  : list of independant variables for the function
               3. X   : symbolic list of the dependant variables in the function f
    
    Output:
               gradient vector as numpy matrix
    """
    lQ = range(0,len(Q))
    lX = range(0,len(x0))
    a = matrix([ Q[j].subs( [ ( X[i],x0[i] ) for i in lX ] ) for j in lQ],'float')
    return matrix(a.reshape(len(Q)**0.5,len(Q)**0.5))
  
def sDescent(f,x0,X):
    """
    Description : Returns the minimizer using the Steepest Descent Algorithm
    
    Parameters:
               1. f   : symbolic representation of the function to be minimized
               2. x0  : list of independant variables for the function
               3. X   : symbolic list of the dependant variables in the function f
    
    Output:
               Prints the minimizer of the function f to terminal
    """
    def stepSizeSteepestDescent(f,x0,g0):
        """
        Description : Calculates the minimized step size for the steepest descent algorithm using Newton's 1D method
    
        Parameters:
                   1. f   : symbolic symbolic representation of the function f
                   2. x0  : list of independant variables for the function
                   3. g0  : gradient value at point x0 as a numpy matrix
    
        Output:
                   gradient vector as numpy matrix
        """
        phi,alpha = symbols('phi alpha')
        Q = hessian(f,X)
        if (poly(f).is_quadratic):
            return float(g0*g0.transpose()/matrix2numpy(g0*Q*g0.transpose()))
        else:
            xStar = x0 - squeeze(asarray(alpha*g0))
            def alphaValue(phi,a0): return phi.subs([(alpha,a0)])
            a0 = 0.
            phi = fValue(f,xStar)
            while (True):
                a = a0
                a0 = a0 - alphaValue(diff(phi,alpha),a0)/alphaValue(diff(diff(phi,alpha),alpha),a0)
                if (abs(a-a0)<epsilon): return a0
    
    gradF=[f.diff(x) for x in X]
    while(True):
        g0 = gradValue(gradF,x0,X)
        x = x0
        step = stepSizeSteepestDescent(f,x0,g0)
        x0 = [float(i) for i in (x0 - squeeze(asarray(step *g0)))]
        g0 = gradValue(gradF,x0,X)
        if(abs(fValue(f,x0,X) - fValue(f,x,X))< epsilon):
            print "\n+++++++++++++++++++++++++++++STEEPEST DESCENT METHOD+++++++++++++++++++++++++++++"
            print "\nThe minimizer of the function\n\nf = %s \nis at \nx = %s" %(f,x0)
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            return 0


def conjugateGradient(f,x0,X):
    """
    Description : Returns the minimizer using the Conjugate Gradient Algorithm
    
    Parameters:
               1. f   : symbolic representation of the function to be minimized
               2. x0  : list of independant variables for the function
               3. X   : symbolic list of the dependant variables in the function f
    
    Output:
               Prints the minimizer of the function f to terminal
    """
    def printFunction(f,x0):
        """
        Description : Prints the minimizer of the function on the screen
        
        Inputs: 
               f  = symbolic representation of the function to be minimized
               x0 = Initial guess of the minimizer
        """
        print "\n+++++++++++++++++++++++++++++CONJUGATE GRADIENT METHOD+++++++++++++++++++++++++++++"
        print "\nThe minimizer of the function\n\nf = %s \nis at \nx = %s" %(f,x0)
        print "+++++++++++++++++++++++++++++++++++++++++++++++++=============+++++++++++++++++++++++\n"
        return 0
    
    gradF = [f.diff(x) for x in X]
    g0 = gradValue(gradF,x0,X)
    if(all(abs(i) < epsilon for i in squeeze(asarray(g0,'float')))): return printFunction(f,x0)
    Q = matrix2numpy(hessian(f,X))
    d0 = -g0
    while(True):
        alpha = -squeeze(asarray(g0*d0.transpose()))/squeeze(asarray(d0*Q*d0.transpose()))
        x0 = [float(i) for i in (x0 + squeeze(asarray(alpha *d0)))]
        g0 = gradValue(gradF,x0,X)
        if(all(abs(i) < epsilon for i in squeeze(asarray(g0,'float')))): return printFunction(f,x0)
        beta = float(squeeze(asarray(g0*Q*d0.transpose())/squeeze(asarray(d0*Q*d0.transpose()))))
        d0 = -g0 +beta*d0


def newton(f,x0,X):
    """
    Description : Returns the minimizer using Newton's Algorithm
    
    Inputs: 
           f  = symbolic representation of the function to be minimized
           x0 = Initial guess of the minimizer
           X  = list of the function's dependant variables
    
    Outputs: 
           Displays the minimizer on the screen
    """
    
    def printFunction(f,x0):
        """
        Description : Prints the minimizer of the function on the screen
        
        Inputs: 
               f  = symbolic representation of the function to be minimized
               x0 = Initial guess of the minimizer
        """
        print "\n+++++++++++++++++++++++++++++NEWTONS METHOD+++++++++++++++++++++++++++++"
        print "\nThe minimizer of the function\n\nf = %s \nis at \nx = %s\n\nThe value of f is \nf(x) = %f\n "%(f,x0,fValue(f,x0,X))
        print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        return 0
    gradF = [f.diff(x) for x in X]
    hessianF = hessian(f,X)
    while(True):
        g0 = gradValue(gradF,x0,X)
        if(all(abs(i) < epsilon for i in squeeze(asarray(g0,'float')))): return printFunction(f,x0)
        F0 = hessianValue(hessianF,x0,X)
        x0 = x0 - squeeze(asarray((inv(F0)*g0.transpose()).transpose()))