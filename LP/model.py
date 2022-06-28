from random import random

from pulp import *
import csv
import os
import random
from glob import glob
from itertools import cycle
from os.path import exists
from z3 import *
import plotly.graph_objects as go
import random
import plotly.express as px

palette = cycle(px.colors.qualitative.Plotly)

def plot_solution(w, h, n, xs, ys, widths, heights, name, filename):
    r = random.Random(42)

    fig = go.Figure()

    for i in range(n):
        x, y = xs[i], ys[i]
        width, height = widths[i], heights[i]
        fig.add_shape(type="rect",
                      x0=x, y0=y, x1=x + width, y1=y + height,
                      line=dict(
                          color="Black",
                          width=2,
                      ),
                      fillcolor=next(palette), )

    fig.update_shapes(dict(xref='x', yref='y'))

    fig.update_xaxes(range=[0, w],
                     autorange=False,
                     scaleratio=1,
                     dtick=1,
                     rangebreaks=[dict(bounds=[0, w])]
                     # type="category",
                     )
    fig.update_yaxes(range=[0, h],
                     # scaleanchor="x",
                     scaleratio=1,
                     autorange=False,
                     dtick=1,
                     rangebreaks=[dict(bounds=[0, h])]
                     # type="category"
                     )

    fig.update_layout(title=name.upper(), title_x=0.5)
    fig.show()
    # fig.write_image(filename, width=1200, height=1200)

def solve(instance, timeout=300000):
    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    problem = LpProblem("VLSI", LpMinimize)

    h_goal = LpVariable("height", max(y), sum(y), cat=LpInteger)

    p_x = [LpVariable(f"x{i + 1}", 0, max(x), cat=LpInteger) for i in range(n)]
    p_y = [LpVariable(f"y{i + 1}", 0, max(y), cat=LpInteger) for i in range(n)]

    x_pair = [[LpVariable(f"x{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    y_pair = [[LpVariable(f"y{i + 1}{j + 1}", cat=LpBinary) for j in range(n)] for i in range(n)]

    delta = [[[LpVariable(f"d_{i + 1}{j + 1}{k + 1}", 0, 1, cat=LpInteger) for k in range(4)] for j in range(n)] for i in range(n)]
    m = [w, w, sum(y), sum(y)]

    problem += h_goal, "Height of the plate"

    # limit constraint
    for i in range(n):
        problem += x[i] + p_x[i] <= w, f'Within_limits_x{i}'
        problem += y[i] + p_y[i] <= h_goal, f'Within_limits_y{i}'

    for i in range(n):
        for j in range(n):
            if i < j:
                problem += p_x[i] + x[i] <= x[j] + m[0] * delta[i][j][0]
                problem += p_x[j] + x[j] <= x[i] + m[1] * delta[i][j][1]
                problem += p_y[i] + y[i] <= y[j] + m[2] * delta[i][j][2]
                problem += p_y[j] + y[j] <= y[i] + m[3] * delta[i][j][3]

                problem += lpSum(delta[i][j][k].varValue for k in range(4)) <= 3
                # print(lpSum(delta[i][j][k] for k in range(4)))

                # problem += p_x[i] + x[i] <= p_x[j]
                # problem += p_y[i] + y[i] <= p_y[j]

    problem.solve()

    print(problem.status)

    for i in range(n):
        print(f"p_x{i + 1}: ", p_x[i].varValue)
        print(f"p_y{i + 1}: ", p_y[i].varValue)

    return h_goal.varValue

    # print("DELTA")
    # for i in range(n):
    #     for j in range(n):
    #         for k in range(4):
    #             print(delta[i][j][k], delta[i][j][k].varValue)

instance = {
    'w': 8,
    'n':  4,
    'x': [3, 3, 5, 5],
    'p_x': [0, 0, 0, 0],
    'y': [3, 5, 3, 5],
    'p_y': [0, 0, 0, 0]
}

l = solve(instance)

print(l)

#
# solution = instance
# plot_solution(solution['w'],
#                               l,
#                               solution['n'],
#                               solution['p_x'],
#                               solution['p_y'],
#                               solution['x'],
#                               solution['y'],
#                               "test",
#                               "test")


