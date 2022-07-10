import argparse
import os
from itertools import cycle
from os.path import exists
import subprocess
import plotly.graph_objects as go
import random
import plotly.express as px


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


# https://stackoverflow.com/questions/9816816/get-absolute-paths-of-all-files-in-a-directory
def absoluteFilePaths(directory):
    for dir_path, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dir_path, f))


def main():
    parser = argparse.ArgumentParser(description='A python interface to run a Minizinc VLSI model.')

    parser.add_argument("-m", "--model", help="The MiniZinc file to execute",
                        required=True, type=str)
    parser.add_argument("-i", "--input_dir", help="Path to the directory containing the initial instances",
                        required=False, type=str, default="../../instances/dzn")
    parser.add_argument("-o", "--output_dir",
                        help="Path to the directory that will contain the output solutions in .txt format",
                        required=False, type=str, default="../out")
    parser.add_argument("-t", "--timeout", help="Seconds before timeout",
                        required=False, type=int, default=300)
    parser.add_argument("-p", "--plots", help="Whether to save the plots",
                        required=False, action='store_true', default=False)

    args = parser.parse_args()

    input_dir = args.input_dir

    output_dir = os.path.join(args.output_dir, *args.model.split(os.sep)[-1].split(".")[0].split("-"))
    if not exists(output_dir):
        os.makedirs(output_dir)

    if args.plots:
        plots_dir = os.path.join(output_dir, "plots")
        if not exists(plots_dir):
            os.makedirs(plots_dir)

    solutions_file = os.path.join(output_dir, 'solutions.csv')

    with open(solutions_file, 'w') as csv_file:
        csv_file.write("name,time,h,valid,optimal\n")

    for file in sorted(absoluteFilePaths(input_dir)):
        if not file.endswith(".dzn"):
            continue

        name = file.split(os.sep)[-1].split('.')[0]
        print(f"Solving instance {name}")
        out_name = name.lower().replace("ins", "out")

        command = f'minizinc -s --time-limit {args.timeout * 1000} --solver chuffed -f {os.path.abspath(args.model)} {os.path.abspath(file)}'

        result = subprocess.getoutput(command)

        time = args.timeout
        h = None
        valid = False
        optimal = False

        while result.split(os.linesep)[0].startswith('%') or result.split(os.linesep)[0].startswith('WARNING'):
            if "solveTime" in result.split(os.linesep)[0]:
                time = float(result.split(os.linesep)[0].split("=")[-1])
            result = os.linesep.join(result.split(os.linesep)[1:])

        if result.split(os.linesep)[0] == "=====UNKNOWN=====":
            print(f"Could not find a result for instance {name}")

        else:
            try:
                w = int(result.split(os.linesep)[0])
            except ValueError:
                print("Could not parse w as int. Output was:")
                print(result)
                exit(1)
            h = int(result.split(os.linesep)[1])
            n = int(result.split(os.linesep)[2])
            p_x = result.split(os.linesep)[3].replace('[', '').replace(']', '')
            p_x = [int(s) for s in p_x.split(',')]
            p_y = result.split(os.linesep)[4].replace('[', '').replace(']', '')
            p_y = [int(s) for s in p_y.split(',')]
            x = result.split(os.linesep)[5].replace('[', '').replace(']', '')
            x = [int(s) for s in x.split(',')]
            y = result.split(os.linesep)[6].replace('[', '').replace(']', '')
            y = [int(s) for s in y.split(',')]

            with open(os.path.join(output_dir, out_name + ".txt"), 'w') as f:
                f.write(f"{w} {h}\n")
                f.write(f"{n}\n")

                for i in range(n):
                    f.write(f"{x[i]} {y[i]} {p_x[i]} {p_y[i]}\n")

            if args.plots:
                plot_name = os.path.join(plots_dir, out_name + '.png')
                plot_solution(w, h, n, p_x, p_y, x, y, name, plot_name)

            if result.split(os.linesep)[7] == "----------":
                valid = True

            if result.split(os.linesep)[8] == "==========":
                optimal = True

        with open(solutions_file, 'a') as csv_file:
            csv_file.write(
                f"{name},{time:.5f},{h},{valid},{optimal}\n")


if __name__ == '__main__':
    main()
