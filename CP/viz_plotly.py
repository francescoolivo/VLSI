import random

import plotly.graph_objects as go
import numpy as np
import matplotlib
import sys
import random
import plotly.express as px
from itertools import cycle
palette = cycle(px.colors.qualitative.Plotly)

def plot_solution(w, h, n, xs, ys, widths, heights, instance=""):
    r = random.Random(42)

    fig = go.Figure()

    fig.update_xaxes(range=[0, w])
    fig.update_yaxes(
        range=[0, h],
        scaleanchor="x",
        scaleratio=1,
    )

    for i in range(n):

        color = r.randint(0, 256 ** 3)

        x, y = xs[i], ys[i]
        width, height = widths[i], heights[i]
        fig.add_shape(type="rect",
                      x0=x, y0=y, x1=x+width, y1=y+height,
                      line=dict(
                          color="Black",
                          width=2,
                      ),
                      fillcolor=next(palette),)

    fig.update_shapes(dict(xref='x', yref='y'))
    fig.show()


if __name__ == "__main__":
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

    plot_solution(w, h, n, x, y, widths, heights, "Solution")