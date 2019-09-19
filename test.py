from sympy import *

x = symbols('x')
a = Integral(cos(x)*exp(x), x)
print(Eq(a, a.doit()))