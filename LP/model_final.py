from pulp import *
from utils import get_min_length, get_max_length


def solve(instance):

    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    problem = LpProblem("VLSI", LpMinimize)

    l_min = get_min_length(x, y, w)
    l_max = get_max_length(x, y, w)

    h_goal = LpVariable("height", lowBound=l_min, upBound=l_max, cat=LpInteger)

    p_x = [LpVariable(f"x{i+1:02d}", 0, w, cat=LpInteger) for i in range(n)]
    p_y = [LpVariable(f"y{i+1:02d}", 0, l_max, cat=LpInteger) for i in range(n)]

    d1 = [[LpVariable(f"d1{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d2 = [[LpVariable(f"d2{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d3 = [[LpVariable(f"d3{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d4 = [[LpVariable(f"d4{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]

    m = [w, w, l_max, l_max]
    problem += h_goal, "main objective"

    # limit constraint
    for i in range(n):
        problem += x[i] + p_x[i] <= w, f'Within_limits_x{i}'
        problem += y[i] + p_y[i] <= h_goal, f'Within_limits_y{i}'

    for i in range(n):
        for j in range(n):
            if i < j:
                # http://amsterdamoptimization.com/pdf/tiling.pdf
                problem += p_x[i] >= p_x[j] + x[j] - m[0] * d1[i][j]
                problem += p_x[i] + x[i] <= p_x[j] + m[1] * d2[i][j]
                problem += p_y[i] >= p_y[j] + y[j] - m[2] * d3[i][j]
                problem += p_y[i] + y[i] <= p_y[j] + m[3] * d4[i][j]
                problem += d1[i][j] + d2[i][j] + d3[i][j] + d4[i][j] <= 3

    problem.solve(GUROBI(msg=False, timeLimit=300))

    p_x_sol = []
    p_y_sol = []

    if problem.status == 1:
        for i in range(n):
            p_x_sol.append(p_x[i].varValue)
            p_y_sol.append(p_y[i].varValue)
        h = h_goal.varValue
    else:
        h = problem.solverModel.getVarByName("height").X
        for i in range(n):
            p_x_sol.append(problem.solverModel.getVarByName(f"x{i+1:02d}").X)
            p_y_sol.append(problem.solverModel.getVarByName(f"y{i+1:02d}").X)



    # storing result
    solution = {'w': w, 'n': n, 'length': h, 'x': x, 'y': y, 'p_x': p_x_sol, 'p_y': p_y_sol,
                'time': problem.solutionTime, 'status': problem.status, 'max_l': l_max}

    return solution



