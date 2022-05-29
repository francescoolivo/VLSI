from z3 import *
import numpy as np
import utils
from itertools import combinations
import time


def solve(instance, timeout=300000):

    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    l_max = utils.get_max_length(x, y, w)

    # index of the circuit with the highest value
    index = np.argmax(np.asarray(y))

    # area of each circuit
    areas = [x[i] * y[i] for i in range(n)]

    # definition of the variables

    # coordinates of the points
    p_x = [Int(f"p_x_{str(i + 1)}") for i in range(n)]
    p_y = [Int(f"p_y_{str(i + 1)}") for i in range(n)]

    # rotation array
    rotation = [Bool("rot_%s" % str(i+1)) for i in range(n)]

    # real dimensions of circuits considering rotation
    x_r = [If(And(x[i] != y[i], rotation[i]), y[i], x[i]) for i in range(n)]
    y_r = [If(And(x[i] != y[i], rotation[i]), x[i], y[i]) for i in range(n)]

    # maximum height to minimize
    # length = utils.z3_max([p_y[i] + y[i] for i in range(n)])
    length = utils.z3_max([p_y[i] + y_r[i] for i in range(n)])

    # domain bounds
    domain_x = [p_x[i] >= 0 for i in range(n)]
    domain_y = [p_y[i] >= 0 for i in range(n)]

    # lengths bound
    width_bound = [And(x_r[i] >= 1, x_r[i] <= w) for i in range(n)]
    height_bound = [And(y_r[i] >= 1, y_r[i] <= l_max) for i in range(n)]

    # different coordinates
    all_different = [Distinct([p_y[i] + p_x[i]]) for i in range(n)]

    # cumulative constraints
    cumulative_y = utils.z3_cumulative(p_y, y_r, x_r, w)
    cumulative_x = utils.z3_cumulative(p_x, x_r, y_r, l_max)

    # maximum width
    max_w = [utils.z3_max([p_x[i] + x_r[i] for i in range(n)]) <= w]

    # maximum height
    max_h = [utils.z3_max([p_y[i] + y_r[i] for i in range(n)]) <= l_max]

    # relationship avoiding overlapping
    overlapping = []
    for (i, j) in combinations(range(n), 2):
        overlapping.append(Or(p_x[i] + x_r[i] <= p_x[j],
                              p_x[j] + x_r[j] <= p_x[i],
                              p_y[i] + y_r[i] <= p_y[j],
                              p_y[j] + y_r[j] <= p_y[i])
                           )

    # the circuit whose height is the maximum among all circuits is put in the left-bottom corner
    symmetry = [And(p_x[index] == 0, p_y[index] == 0)]

    # circuits must be pushed on the left
    left = [sum([If(p_x[i] <= w // 2, areas[i], 0) for i in range(n)])
            >= sum([If(p_x[i] > w // 2, areas[i], 0) for i in range(n)])]

    # setting the optimizer
    opt = Optimize()
    opt.add(domain_x + domain_y + overlapping + all_different + cumulative_x +
            cumulative_y + max_w + max_h + symmetry + width_bound + height_bound + left)
    opt.minimize(length)

    # maximum time of execution
    opt.set("timeout", timeout)

    p_x_sol = []
    p_y_sol = []
    x_sol = []
    y_sol = []

    # solving the problem
    start_time = time.time()


    if opt.check() == sat:
        model = opt.model()
        elapsed_time = time.time() - start_time
        # getting values of variables
        for i in range(n):
            p_x_sol.append(model.evaluate(p_x[i]).as_long())
            p_y_sol.append(model.evaluate(p_y[i]).as_long())
            x_sol.append(model.evaluate(x_r[i]).as_long())
            y_sol.append(model.evaluate(y_r[i]).as_long())


        length_sol = model.evaluate(length).as_long()

        # storing result
        solution = {'w': w, 'n': n, 'length': length_sol, 'x': x_sol, 'y': y_sol, 'p_x': p_x_sol, 'p_y': p_y_sol,
                    'time': elapsed_time, 'found': True}

    else:
        elapsed_time = time.time() - start_time
        solution = {'found': False, 'time': elapsed_time}

    return solution




