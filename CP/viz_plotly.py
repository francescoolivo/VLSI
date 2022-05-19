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

    fig.update_layout(title = name.upper(), title_x=0.5)
    #fig.show()
    fig.write_image(filename, width=1200, height=1200)


if __name__ == "__main__":

    name = sys.argv[1].split('/')[-1].split('.')[0]
    filename = os.path.join(sys.argv[2], f'{name}.png')

    print("="*20)
    print(f"instance {name} started")

    # read compilation stats (useless)
    for i in range(7):
        sys.stdin.readline()
    
    optimality_check = None
    # read solution
    try:
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

        plot_solution(w, h, n, x, y, widths, heights, name, filename)

        # read 2 separator-lines
        sys.stdin.readline()
        optimality_check = sys.stdin.readline()
        if not "%" in optimality_check:
            optimal = True
        else:
            optimal = False

        valid = True
    except ValueError as e:
        print(f"instance {name} returned an error (type 1)\n{e}")
        valid = False
        optimal = False

    # read solving stats
    if optimal:
        initTime = float(sys.stdin.readline().strip().split('=')[-1])
    elif not valid:
        initTime = float(sys.stdin.readline().strip().split('=')[-1])
    else:
        initTime = float(optimality_check.strip().split('=')[-1])
    solveTime = float(sys.stdin.readline().strip().split('=')[-1])
    solutions = int(sys.stdin.readline().strip().split('=')[-1])
    variables = int(sys.stdin.readline().strip().split('=')[-1])
    propagators = int(sys.stdin.readline().strip().split('=')[-1])
    propagations = int(sys.stdin.readline().strip().split('=')[-1])
    nodes = int(sys.stdin.readline().strip().split('=')[-1])
    failures = int(sys.stdin.readline().strip().split('=')[-1])
    restarts = int(sys.stdin.readline().strip().split('=')[-1])
    peakDepth = int(sys.stdin.readline().strip().split('=')[-1])
    # try:
    #     peakDepth = int(sys.stdin.readline().strip().split('=')[-1])
    # except ValueError as e:
    #     print(f"instance {name} returned an error (type 2)")
    #     peakDepth = None

    csv_name = sys.argv[3]

    if not os.path.exists(csv_name):
        f = open(csv_name, mode = "w")
        f.write("instance,init_time,solve_time,solutions,variables,propagators,propagations,nodes,failures,restarts,peak_depth,valid,optimal\n")
    else:
        f = open(csv_name, "a")

    f.write(f'{name},{initTime},{solveTime},{solutions},{variables},{propagators},{propagations},{nodes},{failures},{restarts},{peakDepth},{1 if valid else 0},{1 if optimal else 0}\n')
    f.close()
    
    # print("% Minizinc statics:")
    # print("%%%SolveTime={}\n%%%Propagations={}\n%%%Failures={}".format(solveTime, propagations, failures))

    
    print(f"instance {name} concluded")
    print("="*20)
