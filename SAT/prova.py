from pysmt.shortcuts import Symbol, Or, ForAll, GE, LT, Real, Plus
from pysmt.shortcuts import qelim, is_sat
from pysmt.typing import REAL
from pysmt.solvers.solver import *
from pysmt.formula import FormulaManager
from pysmt.solvers.options import SolverOptions
from pysmt.logics import *

x, y, z = [Symbol(s, REAL) for s in "xyz"]

# # circuits must be pushed on the left
# left =  [GE(Plus(*[Ite(LE(p_x[i], Int(w // 2)), Int(areas[i]), Int(0))for i in range(n)]),
#                 Plus(*[Ite(GT(p_x[i], Int(w // 2)), Int(areas[i]), Int(0)) for i in range(n)]))]

Solver = Solver(FormulaManager, AUTO)


f = ForAll([x], Or(LT(x, Real(5.0)),
                   GE(Plus(x, y, z), Real((17,2))))) # (17,2) ~> 17/2

Solver.push()
Solver.add_assertion(GE(x, Real(6.0)))
print("f := %s" % f)
#f := (forall x . ((x < 5.0) | (17/2 <= (x + y + z))))

qf_f = qelim(f, solver_name="z3")
print("Quantifier-Free equivalent: %s" % qf_f)
#Quantifier-Free equivalent: (7/2 <= (z + y))

res = is_sat(qf_f, solver_name="msat")
print("SAT check using MathSAT: %s" % res)
#SAT check using MathSAT: True