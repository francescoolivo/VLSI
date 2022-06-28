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
                      fillcolor=next(palette),
                      opacity=0.5)

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

def get_max_length(x, y, w):
    # int: l_max = ceil( l_min + sum(heights) / 2);

    l_min = get_min_length(x, y, w)
    heights_sum = 0
    for i in y:
        heights_sum += i

    l_max = math.ceil(l_min + heights_sum / 2)
    return l_max


def get_min_length(x, y , w):
    #int: l_min = max(heights + +  [ceil(sum([heights[i] * widths[i] | i in 1..n]) / w)]);
    area_sum = 0
    for i in range(len(x)):
        area_sum += x[i] * y[i]

    values = [math.ceil(area_sum / w)] + y
    return max(values)

def solve(instance, timeout=300000):
    w = instance['w']
    n = instance['n']
    x = instance['x']
    y = instance['y']

    problem = LpProblem("VLSI", LpMinimize)

    l_min = get_min_length(x, y, w)
    l_max = get_max_length(x, y, w)

    print(l_min, l_max)

    h_goal = LpVariable("height", lowBound=l_min, upBound=l_max, cat=LpInteger)

    p_x = [LpVariable(f"x{i + 1}", 0, w, cat=LpInteger) for i in range(n)]
    p_y = [LpVariable(f"y{i + 1}", 0, l_max, cat=LpInteger) for i in range(n)]

    d1 = [[LpVariable(f"d1{i+1}{j+1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d2 = [[LpVariable(f"d2{i+1}{j+1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d3 = [[LpVariable(f"d3{i+1}{j+1}", cat=LpBinary) for j in range(n)] for i in range(n)]
    d4 = [[LpVariable(f"d4{i+1}{j+1}", cat=LpBinary) for j in range(n)] for i in range(n)]

    m = [w, w, l_max, l_max]
    problem += h_goal, "Height of the plate"

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

    problem.solve()

    print(problem.status)

    return p_x, p_y, h_goal

instance = {
    'w': 9,
    'n':  5,
    'x': [3, 3, 3, 3, 3],
    'p_x': [],
    'y': [3, 4, 5, 6, 9],
    'p_y': []
}

# instance = {
#     'w': 9,
#     'n':  5,
#     'x': [3, 3, 3, 3, 3],
#     'p_x': [3, 3, 3, 6, 0],
#     'y': [3, 4, 5, 6, 9],
#     'p_y': [9, 5, 0, 0, 0]
# }

p_x, p_y, l = solve(instance)
l = l.varValue
print(l)

for i in range(instance['n']):
    instance['p_x'].append(int(p_x[i].varValue))
    instance['p_y'].append(int(p_y[i].varValue))

solution = instance
print(solution)
plot_solution(solution['w'],
              l,
              solution['n'],
              solution['p_x'],
              solution['p_y'],
              solution['x'],
              solution['y'],
              "test",
              "test")


