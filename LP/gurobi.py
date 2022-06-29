import math
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import matplotlib.pyplot as plt
import numpy as np

w = 9
n = 5
widhts = [3, 3, 3, 3, 3]
heights = [3, 4, 5, 6, 9]

x = [None] * n
y = [None] * n

# MIN
area_sum = 0
for i in range(len(x)):
    area_sum += widhts[i] * heights[i]

values = [math.ceil(area_sum / w)] + heights
print(values)
l_min = max(values)
# MAX
heights_sum = 0
for i in heights:
    heights_sum += i
l_max = math.ceil(l_min + heights_sum / 2)

# Model
m = gp.Model("problem")

for i in range(n):
    x[i] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=w, name=f'x{i}')
    y[i] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=l_max, name=f'y{i}')

d1 = [[None] * n] * n
d2 = [[None] * n] * n
d3 = [[None] * n] * n
d4 = [[None] * n] * n

for i in range(n):
    for j in range(n):
        d1[i][j] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name=f'd1[i][j]')
        d2[i][j] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name=f'd2[i][j]')
        d3[i][j] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name=f'd3[i][j]')
        d4[i][j] = m.addVar(vtype=GRB.INTEGER, lb=0, ub=1, name=f'd4[i][j]')

me = [w, w, l_max, l_max]

l = m.addVar(vtype=GRB.INTEGER, lb=l_min, ub=l_max, name='l')

m.setObjective(l, GRB.MINIMIZE)

# Constraints
for i in range(n):
    m.addConstr(x[i] + widhts[i] <= w, f'Main_Constraint_X{i}')
    m.addConstr(y[i] + heights[i] <= l, f'Main_Constraint_Y{i}')

for i in range(n):
    for j in range(n):
        if (i < j):
            m.addConstr(x[i] >= x[j] + widhts[j] - me[0] * d1[i][j])
            m.addConstr(x[i] + widhts[i] <= x[j] + me[1] * d2[i][j])
            m.addConstr(y[i] >= y[j] + heights[j] - me[2] * d3[i][j])
            m.addConstr(y[i] + heights[i] <= y[j] + me[3] * d4[i][j])
            m.addConstr(d1[i][j] + d2[i][j] + d3[i][j] + d4[i][j] <= 3)

m.optimize()

xs = [None] * n
ys = [None] * n
for i in range(n):
    xs[i] = int(x[i].X)
    ys[i] = int(y[i].X)
    print(f"X{i + 1}: ", x[i])
    print(f"Y{i + 1}: ", y[i])


def plot_solution(w, h, n, xs, ys, widths, heights, instance=""):
    image = np.ones((h, w, 3))
    np.random.seed(42)

    for i in range(n):
        x, y = xs[i], ys[i]
        width, height = widths[i], heights[i]
        image[y:y + height, x:x + width] = np.random.random(3)

    plt.matshow(image[::-1])
    plt.tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    plt.title("Instance " + instance)
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, w, 1))
    ax.set_yticks(np.arange(-.5, h, 1))
    ax.set_xticklabels(np.arange(0, w + 1, 1))
    ax.set_yticklabels(np.arange(h, -1, -1))

    plt.show()


h = int(l.X)

plot_solution(w, h, n, xs, ys, widhts, heights)