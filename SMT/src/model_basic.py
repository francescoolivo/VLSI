import numpy as np
from itertools import combinations
import time
from utils import get_min_length, get_max_length
from pysmt.shortcuts import *


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


def solve(instance, timeout=300):
    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    l_max = get_max_length(x, y, w)
    l_min = get_min_length(x, y, w)

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y) * np.asarray(x))

    # definition of the variables

    # coordinates of the points
    p_x = [Symbol(f"p_x_{str(i + 1)}", INT) for i in range(n)]
    p_y = [Symbol(f"p_y_{str(i + 1)}", INT) for i in range(n)]

    h = Symbol("h", INT)

    domain_x = [GE(p_x[i], Int(0)) for i in range(n)]
    domain_y = [GE(p_y[i], Int(0)) for i in range(n)]

    main_constraint = []
    for i in range(n):
        main_constraint.append(LE(p_x[i] + x[i], Int(w)))
        main_constraint.append(LE(p_y[i] + y[i], h))

    # cumulative constraints
    cumulative_y = smt_cumulative(p_y, y, x, w)
    cumulative_x = smt_cumulative(p_x, x, y, l_max)

    # relationship avoiding overlapping
    overlapping = []
    for (i, j) in combinations(range(n), 2):
        overlapping.append(Or(LE(p_x[i] + x[i], p_x[j]),
                              LE(p_x[j] + x[j], p_x[i]),
                              LE(p_y[i] + y[i], p_y[j]),
                              LE(p_y[j] + y[j], p_y[i]),
                              ))

    full_bottom = Equals(Plus(*[Ite(Equals(p_y[i], Int(0)), Int(x[i]), Int(0)) for i in range(n)]), Int(w))

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(Equals(p_x[index], Int(0))), Equals(p_y[index], Int(0))]

    k = l_min
    # setting the optimizer
    formula = And(Equals(h, Int(k)), *symmetry, *domain_x, *domain_y, *main_constraint,
                  *overlapping, *cumulative_x, *cumulative_y, full_bottom)

    start_time = time.time()

    # {z3->timeout - cvc4->tlimit} solver_options={"timeout": 300*1000}
    with Solver(name="z3", solver_options={"timeout": timeout * 1000, "auto_config": True}) as solver:
        solver.add_assertion(formula)
        try:
            while not solver.is_sat(formula):
                k = k + 1
                formula = And(Equals(h, Int(k)), *symmetry, *domain_x, *domain_y, *main_constraint,
                              *overlapping, *cumulative_x, *cumulative_y, full_bottom)
                solver.reset_assertions()
                solver.add_assertion(formula)

            model = solver.get_model()
            h = model.get_value(h).constant_value()
        except:
            elapsed_time = time.time() - start_time
            solution = {'w': w, 'n': n, 'length': h, 'x': x, 'y': y, 'p_x': [], 'p_y': [],
                        'time': elapsed_time, 'found': False}
            return solution

    elapsed_time = time.time() - start_time
    p_x_sol = []
    p_y_sol = []

    for i in range(n):
        p_x_sol.append(model.get_value(p_x[i]).constant_value())
        p_y_sol.append(model.get_value(p_y[i]).constant_value())

    solution = {'w': w, 'n': n, 'length': h, 'x': x, 'y': y, 'p_x': p_x_sol, 'p_y': p_y_sol,
                'time': elapsed_time, 'found': True}
    return solution