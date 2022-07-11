from pulp import *
from utils import get_min_length, get_max_length
import numpy as np


def solve(instance, timeout=300, symmetry=False):
    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    index = np.argmax(np.asarray(y) * np.asarray(x))

    l_min = get_min_length(x, y, w)
    l_max = get_max_length(x, y, w)

    l_goal = LpVariable("height", lowBound=l_min, upBound=l_max, cat=LpInteger)

    p_x = [LpVariable(f"x{i + 1:02d}", lowBound=0, upBound=w - min(x), cat=LpInteger) for i in range(n)]
    p_y = [LpVariable(f"y{i + 1:02d}", lowBound=0, upBound=l_max - min(y), cat=LpInteger) for i in range(n)]

    d1 = [[LpVariable(f"d1{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d2 = [[LpVariable(f"d2{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d3 = [[LpVariable(f"d3{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d4 = [[LpVariable(f"d4{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]

    problem = LpProblem("VLSI", LpMinimize)

    m = [w, w, l_max, l_max]
    problem += l_goal, "main objective"

    # limit constraint
    for i in range(n):
        problem += x[i] + p_x[i] <= w, f'Within_limits_x{i}'
        problem += y[i] + p_y[i] <= l_goal, f'Within_limits_y{i}'

    for i in range(n):
        for j in range(n):
            if i < j:
                problem += p_x[i] >= p_x[j] + x[j] - m[0] * d1[i][j]
                problem += p_x[i] + x[i] <= p_x[j] + m[1] * d2[i][j]
                problem += p_y[i] >= p_y[j] + y[j] - m[2] * d3[i][j]
                problem += p_y[i] + y[i] <= p_y[j] + m[3] * d4[i][j]
                problem += d1[i][j] + d2[i][j] + d3[i][j] + d4[i][j] <= 3

    # larger plate in 0,0
    problem += p_x[index] == 0
    problem += p_y[index] == 0

    if symmetry:
        # change if the path is different
        path_to_cplex = "/opt/ibm/ILOG/CPLEX_Studio221/cplex/bin/x86-64_linux/cplex"
        solver = CPLEX_CMD(path=path_to_cplex, msg=False, timeLimit=timeout,
                           options=["set preprocessing symmetry 5"])
    else:
        solver = CPLEX_PY(msg=False, timeLimit=timeout)

    # GUROBI
    # solver = GUROBI(msg=False, timeLimit=timeout)

    problem.solve(solver)

    p_x_sol = []
    p_y_sol = []

    if problem.status == 1:
        for i in range(n):
            p_x_sol.append(round(p_x[i].varValue))
            p_y_sol.append(round(p_y[i].varValue))
        l = round(l_goal.varValue)

    else:
        try:
            l = round(problem.solverModel.getVarByName("height").X)
            for i in range(n):
                p_x_sol.append(round(problem.solverModel.getVarByName(f"x{i + 1:02d}").X))
                p_y_sol.append(round(problem.solverModel.getVarByName(f"y{i + 1:02d}").X))
        except:
            solution = {'w': w, 'n': n, 'length': 0, 'x': x, 'y': y, 'p_x': [], 'p_y': [],
                        'time': problem.solutionTime, 'status': -1, 'max_l': l_max}
            return solution

    # storing result
    solution = {'w': w, 'n': n, 'length': l, 'x': x, 'y': y, 'p_x': p_x_sol, 'p_y': p_y_sol,
                'time': problem.solutionTime, 'status': l - l_min, 'max_l': l_max}

    return solution
