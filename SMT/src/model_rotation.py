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
                Ite(And(LE(start[i], resource), LT(resource, start[i] + duration[i])),
                    resources[i], Int(0))
                for i in range(len(start))]),
               Int(total))
        )
    return decomposition


def solve(instance, timeout=300):
    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    l_min = get_min_length(x, y, w)
    l_max = get_max_length(x, y, w)

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y) * np.asarray(x))

    # definition of the variables

    # coordinates of the points
    r = [Symbol(f"r_{str(i + 1)}") for i in range(n)]
    p_x = [Symbol(f"p_x_{str(i + 1)}", INT) for i in range(n)]
    p_y = [Symbol(f"p_y_{str(i + 1)}", INT) for i in range(n)]

    x_r = [Ite(r[i], Int(y[i]), Int(x[i])) for i in range(n)]
    y_r = [Ite(r[i], Int(x[i]), Int(y[i])) for i in range(n)]

    l = Symbol("l", INT)

    domain_x = [And(GE(p_x[i], Int(0)), LE(p_x[i], Int(w) - Min(x_r))) for i in range(n)]
    domain_y = [And(GE(p_y[i], Int(0)), LE(p_y[i], Int(l_max) - Min(y_r))) for i in range(n)]

    domain_l = And(GE(l, Int(l_min)), LE(l, Int(l_max)))

    main_constraint = []
    for i in range(n):
        main_constraint.append(LE(p_x[i] + x_r[i], Int(w)))
        main_constraint.append(LE(p_y[i] + y_r[i], l))

    symmetry_rotation = []
    for i in range(n):
        if (x[i] == y[i]):
            symmetry_rotation.append(Iff(r[i], FALSE()))
        if (y[i] > w):
            symmetry_rotation.append(Iff(r[i], FALSE()))

    # cumulative constraints
    # cumulative_y = smt_cumulative(p_y, y_r, x_r, w)
    # cumulative_x = smt_cumulative(p_x, x_r, y_r, l_max)

    # relationship avoiding overlapping
    overlapping = []
    for (i, j) in combinations(range(n), 2):
        overlapping.append(Or(LE(p_x[i] + x_r[i], p_x[j]),
                              LE(p_x[j] + x_r[j], p_x[i]),
                              LE(p_y[i] + y_r[i], p_y[j]),
                              LE(p_y[j] + y_r[j], p_y[i]),
                              ))

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(Equals(p_x[index], Int(0))), Equals(p_y[index], Int(0))]

    full_bottom = Equals(Plus(*[Ite(Equals(p_y[i], Int(0)), x_r[i], Int(0)) for i in range(n)]), Int(w))

    k = l_min

    # setting the optimizer
    formula = And(Equals(l, Int(k)), *domain_x, *domain_y, domain_l, *main_constraint,
                  *overlapping, *symmetry_rotation, *symmetry, full_bottom)

    start_time = time.time()

    # cvc4 -> Solver(name="cvc4", solver_options={"tlimit": 300*1000})
    with Solver(name="z3", solver_options={"timeout": timeout * 1000, "auto_config": True}) as solver:
        solver.add_assertion(formula)
        try:
            while not solver.is_sat(formula):
                k = k + 1
                formula = And(Equals(l, Int(k)), *domain_x, *domain_y, domain_l, *main_constraint,
                              *overlapping, *symmetry_rotation, *symmetry, full_bottom)
                solver.reset_assertions()
                solver.add_assertion(formula)

            model = solver.get_model()
            l = model.get_value(l).constant_value()
        except:
            elapsed_time = time.time() - start_time
            print("errore")
            solution = {'w': w, 'n': n, 'length': l, 'x': x, 'y': y, 'p_x': [], 'p_y': [],
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

    solution = {'w': w, 'n': n, 'length': l, 'x': x, 'y': y, 'p_x': p_x_sol, 'p_y': p_y_sol,
                'time': elapsed_time, 'found': True}
    return solution
