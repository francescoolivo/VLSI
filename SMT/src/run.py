import argparse
import random
from itertools import cycle
from os.path import exists
import os
import plotly.express as px
import plotly.graph_objects as go
import model_basic
import model_rotation
import utils


def plot_solution(w, h, n, xs, ys, widths, heights, name, filename):
    palette = cycle(px.colors.qualitative.Plotly)

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
    # fig.show()
    fig.write_image(filename, width=1200, height=1200)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str, default="../../instances/txt")
    parser.add_argument("-o", "--output_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str, default="../out")
    parser.add_argument("-r", "--rotation", help="Flag to decide whether to allow rotation",
                        required=False, action='store_true', default=False)
    parser.add_argument("-t", "--timeout", help="Seconds before timeout",
                        required=False, type=int, default=300)
    parser.add_argument("-p", "--plots", help="Whether to save the plots",
                        required=False, action='store_true', default=False)

    args = parser.parse_args()

    # model to execute
    if args.rotation:
        model = "rotation"
    else:
        model = "basic"

    input_dir = args.input_dir
    output_dir = os.path.join(args.output_dir, model)
    if not exists(output_dir):
        os.makedirs(output_dir)

    plots_dir = os.path.join(output_dir, "plots")
    if not exists(plots_dir) and args.plots:
        os.makedirs(plots_dir)

    solutions_file = os.path.join(output_dir, 'solutions.csv')

    with open(solutions_file, 'w') as csv_file:
        csv_file.write("name,time\n")

    for file in sorted(os.listdir(input_dir)):
        if file.endswith(".txt"):
            name = file.split(os.sep)[-1].split('.')[0]
            out_name = name.lower().replace("ins", "out")

            instance = utils.read_file(os.path.join(input_dir, file))
            print(f"Solving instance {name}")

            if args.rotation:
                solution = model_rotation.solve(instance, args.timeout)
            else:
                solution = model_basic.solve(instance, args.timeout)

            if solution['found']:
                plot_name = os.path.join(plots_dir, out_name + '.png')
                if args.plots:
                    plot_solution(solution['w'],
                                  solution['length'],
                                  solution['n'],
                                  solution['p_x'],
                                  solution['p_y'],
                                  solution['x'],
                                  solution['y'],
                                  name,
                                  plot_name)
                utils.write_file(os.path.join(output_dir, out_name + ".txt"), solution)
                print(f"Solution found in time {solution['time']:.3f}")
            else:
                print("Solution not found in time")

            with open(solutions_file, 'a') as csv_file:
                csv_file.write(f"{name},{solution['time']:.5f}\n")


if __name__ == '__main__':
    main()
