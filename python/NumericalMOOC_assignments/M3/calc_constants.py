import sympy
import numpy

    # Creating symbolic variables using SymPy function symbols()

u_max,u_star,rho_max,rho_star,A,B,F, rho= sympy.symbols('u_max u_star rho_max rho_star A B F rho')

    # Creating equations using SymPy function Eq(); sympy.Eq(lhs,rhs)


eq1 = sympy.Eq(0,u_max*rho_max*(1-A*rho_max-B*rho_max**2))
eq2 = sympy.Eq(0,u_max*(1-2*A*rho_star-3*B*rho_star**2))
eq3 = sympy.Eq(u_star,u_max*(1-A*rho_star-B*rho_star**2))

eq4 = sympy.Eq(eq2.lhs-3*eq3.lhs,eq2.rhs-3*eq3.rhs)

#    Creating symbolic solutions of the equations created above
#    using the SymPy function solve().


rho_sol = sympy.solve(eq4,rho_star)[0]

b_sol = sympy.solve(eq1,B)[0]

#    Creating a Qaudratic Equation in A by substituting above variables
#    in Equation 2 using the SymPy function subs().


quadA = eq2.subs([(rho_star,rho_sol),(B,b_sol)])

#    solving quadratic to give find the roots

a_sol = sympy.solve(quadA,A)


#    Finding values of A and B based on values of rho_max,u_max,u_star
#    using the symPy function evalf()


aVal = a_sol[1].evalf(subs={rho_max:15.,u_max:2.,u_star:1.5})

if aVal < 0 :
    aVal = a_sol[0].evalf(subs={rho_max:15.,u_max:2.,u_star:1.5})

bVal = b_sol.evalf(subs={rho_max:15.,A:aVal})

#     Creating a equation to caluculate theoretical maximum value
#     of rho before the wave changes sign

maxF = sympy.diff(2.*rho*(1-aVal*rho-bVal*rho**2),rho)

rhoMaxTheoretical =  sympy.solve(maxF,rho)[len(numpy.where(sympy.solve(maxF,rho)>0))]

print "\nThe Value of A is: A = ",'%0.5f' %aVal , "\n"
print "The Value of B is: B = ",'%0.5f' %bVal , "\n"
print "The Theoretical Maximum Value of rho is ","%0.2f" %rhoMaxTheoretical,"\n"
