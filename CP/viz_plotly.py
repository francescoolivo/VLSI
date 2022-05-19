import random
import os
import plotly.graph_objects as go
import numpy as np
import matplotlib
import sys
import random
import plotly.express as px
from itertools import cycle

palette = cycle(px.colors.qualitative.Plotly)


def plot_solution(w, h, n, xs, ys, widths, heights, instance, filename):
    r = random.Random(42)

    fig = go.Figure()

    for i in range(n):
        color = r.randint(0, 256 ** 3)

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

    fig.update_layout(title = name)
    #fig.show()
    fig.write_image(filename, width=600, height=600)


if __name__ == "__main__":

    name = sys.argv[1].split('.')[0]
    filename = os.path.join(sys.argv[2], f'{name}.png')

    # read compilation stats (useless)
    for i in range(7):
        sys.stdin.readline()
    
    # read solution
    w = int(sys.stdin.readline())
    h = int(sys.stdin.readline())
    n = int(sys.stdin.readline())
    x_str = sys.stdin.readline().strip().replace('[', '').replace(']', '')
    x = [int(s) for s in x_str.split(',')]
    y_str = sys.stdin.readline().strip().replace('[', '').replace(']', '')
    y = [int(s) for s in y_str.split(',')]
    w_str = sys.stdin.readline().strip().replace('[', '').replace(']', '')
    widths = [int(s) for s in w_str.split(',')]
    h_str = sys.stdin.readline().strip().replace('[', '').replace(']', '')
    heights = [int(s) for s in h_str.split(',')]

    # read 2 separator-lines
    for i in range(2):
        sys.stdin.readline()

    # read solving stats
    initTime = float(sys.stdin.readline().strip().split('=')[-1])
    solveTime = float(sys.stdin.readline().strip().split('=')[-1])
    solutions = int(sys.stdin.readline().strip().split('=')[-1])
    variables = int(sys.stdin.readline().strip().split('=')[-1])
    propagators = int(sys.stdin.readline().strip().split('=')[-1])
    propagations = int(sys.stdin.readline().strip().split('=')[-1])
    nodes = int(sys.stdin.readline().strip().split('=')[-1])
    failures = int(sys.stdin.readline().strip().split('=')[-1])
    restarts = int(sys.stdin.readline().strip().split('=')[-1])
    peakDepth = int(sys.stdin.readline().strip().split('=')[-1])

    csv_name = sys.argv[3]

    if not os.path.exists(csv_name):
        f = open(csv_name, mode = "w")
        f.write("init_time,solve_time,solutions,variables,propagators,propagations,nodes,failures,restarts,peak_depth\n")
    else:
        f = open(csv_name, "a")

    f.write(f'{initTime},{solveTime},{solutions},{variables},{propagators},{propagations},{nodes},{failures},{restarts},{peakDepth}\n')
    f.close()
    
    print("% Minizinc statics:")
    print("%%%SolveTime={}\n%%%Propagations={}\n%%%Failures={}".format(solveTime, propagations, failures))

    plot_solution(w, h, n, x, y, widths, heights, name, filename)
