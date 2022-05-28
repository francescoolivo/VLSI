import math
from z3 import *

def read_file(filename):
    with open(filename, 'r') as f:
        w = int(f.readline())
        n = int(f.readline())

        x = []
        y = []

        for line in f.readlines():
            x.append(int(line.split()[0]))
            y.append(int(line.split()[1]))

        return {
            'w': w,
            'n': n,
            'x': x,
            'y': y,
        }


def write_file(filename, args):
    with open(filename, 'w') as f:
        f.write(f"{args['w']} {args['length']}\n")
        f.write(f"{args['n']}\n")

        for i in range(args["n"]):
            f.write(f"{args['x'][i]} {args['y'][i]} {args['p_x'][i]} {args['p_y'][i]}\n")

    return


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

def z3_max(vector):
    maximum = vector[0]
    for value in vector[1:]:
        maximum = If(value > maximum, value, maximum)

    return maximum


def z3_cumulative(start, duration, resources, total):
    decomposition = []
    for resource in resources:
        decomposition.append(
            sum([If(And(start[i] <= resource, resource < start[i] + duration[i]), resources[i], 0)
                 for i in range(len(start))]) <= total
        )
    return decomposition


