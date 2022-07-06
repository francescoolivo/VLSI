from pysmt.typing import *
from pysmt.shortcuts import *
import numpy as np
from itertools import combinations
import time
from utils import get_min_length, get_max_length
from pysmt.solvers import *
from pysmt.logics import *
from pysmt.shortcuts import Equals, Symbol, And, Or, GE, LE, Ite, Int, get_model, ForAll, AllDifferent

#cumulative_y = smt_cumulative(p_y, y, x, w)
def smt_cumulative(start, duration, resources, total):
    decomposition = []
    for resource in resources:
        decomposition.append(
            LE(Plus(*[
                Ite(And(LE(start[i], Int(resource)), LT(Int(resource), start[i] + Int(duration[i]))),
                    Int(resources[i]), Int(0))
                for i in range(len(start))]),
               Int(total))
        )
    return decomposition


w = 4
n = 4
x = [1,1,2,1]
y = [2,2,1,1]

l_max = get_max_length(x, y, w)
l_min = get_min_length(x, y, w)

# index of the circuit with the highest value
index = np.argmax(np.asarray(y) * np.asarray(x))

# area of each circuit
areas = [x[i] * y[i] for i in range(n)]

# definition of the variables

# coordinates of the points
# pxN,W
p_x = [[] for x in range(n)]
p_y = [[] for x in range(n)]

for i in range(n):
    for j in range(w+1):
        p_x[i].append(Symbol(f"p_x_{i+1}_{j}"))
for i in range(n):
    for j in range(l_min+1):
        p_y[i].append(Symbol(f"p_y_{i+1}_{j}"))

l = [[] for x in range(n)]
u = [[] for x in range(n)]
for i in range(n):
    for j in range(n):
        l[i].append(Symbol(f"l_{i+1}_{j+1}"))
        u[i].append(Symbol(f"u_{i+1}_{j+1}"))

order_constraint = []
for i in range(n):
    for j in range(w-x[i]):
        order_constraint.append(Or(Not(p_x[i][j]), p_x[i][j+1]))

for i in range(n):
    for j in range(l_min - y[i]):
        order_constraint.append(Or(Not(p_y[i][j]), p_y[i][j+1]))


non_overlapping1 = []
for i in range(n):
    for j in range(n):
        if i < j:
            non_overlapping1.append(Or( l[i][j], l[j][i], u[i][j], u[j][i]))

non_overlapping2 = []
for i in range(n):
    for j in range(n):
        if i<j :
            for e in range(w - x[i] - 1):
                non_overlapping2.append(Or( Not(l[i][j]), p_x[i][e], Not(p_x[j][e+x[i]])))
                non_overlapping2.append(Or( Not(l[j][i]), p_x[j][e], Not(p_x[i][e+x[j]])))
            for f in range(l_min - y[j] - 1):
                non_overlapping2.append(Or( Not(u[i][j]), p_y[i][f], Not(p_y[j][f+y[i]])))
                non_overlapping2.append(Or( Not(u[j][i]), p_y[j][f], Not(p_y[i][f+y[j]])))

print("--")
print(non_overlapping2)

k = l_min
formula = And(*order_constraint, *non_overlapping1, *non_overlapping2)

start_time = time.time()

with Solver(name="z3") as solver:
    solver.add_assertion(formula)
    try:
        solver.is_sat(formula)
        model = solver.get_model()
        print(model)
    except:
        elapsed_time = time.time() - start_time
        print("errore")
