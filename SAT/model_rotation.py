from pysmt.typing import *
from pysmt.shortcuts import *
import numpy as np
from itertools import combinations
import time
from utils import get_min_length, get_max_length
from pysmt.solvers import *
from pysmt.logics import *
from pysmt.shortcuts import Equals, Symbol, And, Or, GE, LE, Ite, Int, get_model, ForAll, AllDifferent

def smt_max(l: list):
    maximum = l[0]

    for value in l[1:]:

        maximum = Ite(value > maximum, value, maximum)

    return maximum
# cumulative_y = smt_cumulative(r, p_y, y, x, w)
# Ite(r[i], Int(duration[i]), Int(resource))
def smt_cumulative(r, start, duration, resources, total):
    decomposition = []
    for resource in resources:
        decomposition.append(
            LE(Plus(*[
                    Ite(    And(LE( start[i], Ite(r[i], Int(duration[i]), Int(resource)) ), 
                            LT( Ite(r[i], Int(duration[i]), Int(resource)), start[i] + Ite(r[i], Int(resource), Int(duration[i])))),
                            Ite(r[i], Int(duration[i]), Int(resource)), Int(0))
                        for i in range(len(start))]), 
                Int(total))
        )
    return decomposition

def solve(instance, timeout=300000):

    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    l_max = get_max_length(x, y, w)
    l_min = get_min_length(x, y, w)

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y)*np.asarray(x))

    # area of each circuit
    areas = [x[i] * y[i] for i in range(n)]

    # definition of the variables

    # x -> Ite(r[i], y[i], x[i])     
    # y -> Ite(r[i], x[i], y[i])

    # coordinates of the points
    r = [Symbol(f"r_{str(i + 1)}") for i in range(n)]
    p_x = [Symbol(f"p_x_{str(i + 1)}", INT) for i in range(n)]
    p_y = [Symbol(f"p_y_{str(i + 1)}", INT) for i in range(n)]

    h = Symbol("h", INT)


    domain_x = []
    domain_y = []
    #domain_h = [And(GE(h,Int(l_min)), LE(h, Int(l_max)))]

    domain_x = [And(GE(p_x[i], Int(0)), LE(p_x[i], Int(w))) for i in range(n)]
    domain_y = [And(GE(p_y[i], Int(0)), LE(p_y[i], Int(l_max))) for i in range(n)]

    main_constraint = []
    for i in range(n):
        main_constraint.append(LE(p_x[i]+Ite(r[i], Int(y[i]), Int(x[i])) , Int(w)))
        main_constraint.append(LE(p_y[i]+Ite(r[i], Int(x[i]), Int(y[i])), h))


    # cumulative constraints
    cumulative_y = smt_cumulative(r, p_y, y, x, w)
    cumulative_x = smt_cumulative(r, p_x, x, y, l_max)

    # maximum height
    max_h = []
    max_w = []
    for i in range(n):
        max_h.append(LE(p_y[i] + Ite(r[i], Int(x[i]), Int(y[i])) , Int(l_max)))
        max_w.append(LE(p_x[i] + Ite(r[i], Int(y[i]), Int(x[i]))  ,Int(w)))


    # relationship avoiding overlapping
    overlapping = []
    for (i, j) in combinations(range(n), 2):
        overlapping.append(Or(  LE(p_x[i] + Ite(r[i], Int(y[i]), Int(x[i])) ,p_x[j]),
                                LE(p_x[j] + Ite(r[j], Int(y[j]), Int(x[j])) ,p_x[i]),
                                LE(p_y[i] + Ite(r[i], Int(x[i]), Int(y[i])) ,p_y[j]),
                                LE(p_y[j] + Ite(r[j], Int(x[j]), Int(y[j])) ,p_y[i]),
                           ))

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(Equals(p_x[index], Int(0))), Equals(p_y[index], Int(0))]

    k = l_min 
    # setting the optimizer
    formula = And(Equals(h, Int(k)), *domain_x, *domain_y,*main_constraint,
                     *overlapping, *max_w, *max_h, *cumulative_x, *cumulative_y)

    start_time = time.time()
    #{z3->timeout - cvc4->tlimit} solver_options={"timeout": 300*1000}

    with Solver(name="z3",solver_options={"timeout": 300*1000, "unsat_core" : True, "auto_config" : True}) as solver:
        solver.add_assertion(formula)
        try:
            while not solver.is_sat(formula):
                    k = k + 1
                    formula = And(*domain_x,*cumulative_x, *cumulative_y,
                                    *domain_y, *main_constraint, *overlapping, *max_w, *max_h, Equals(h, Int(k)))
                    solver.reset_assertions()
                    solver.add_assertion(formula)

            model = solver.get_model()
            h = model.get_value(h).constant_value()
        except:
            elapsed_time = time.time() - start_time
            print("errore")   
            solution = {'w': w, 'n': n, 'length': h, 'x': x, 'y': y, 'p_x': [], 'p_y': [],
                     'time': elapsed_time, 'found': False}
            return solution

    elapsed_time = time.time() - start_time
    p_x_sol = []
    p_y_sol = []

    for i in range(n):
        p_x_sol.append(model.get_value(p_x[i]).constant_value())
        p_y_sol.append(model.get_value(p_y[i]).constant_value())
        if model.get_value(r[i]).constant_value():
            x[i], y[i] = y[i], x[i]

    solution = {'w': w, 'n': n, 'length': h, 'x': x, 'y': y, 'p_x': p_x_sol, 'p_y': p_y_sol,
                     'time': elapsed_time, 'found': True}
    return solution