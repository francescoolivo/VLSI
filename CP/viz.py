import matplotlib.pyplot as plt
import numpy as np
import sys


def plot_solution(w, h, n, xs, ys, widths, heights, instance=""):
    image = np.ones((h, w, 3))
    np.random.seed(42)

    for i in range(n):
        x, y = xs[i], ys[i]
        width, height = widths[i], heights[i]
        image[y:y+height, x:x+width] = np.random.random(3)

    plt.matshow(image[::-1])
    plt.tick_params(top=False, labeltop=False, bottom=True, labelbottom=True)
    plt.title("Instance " + instance)
    ax = plt.gca()
    ax.set_xticks(np.arange(-.5, w, 1))
    ax.set_yticks(np.arange(-.5, h, 1))
    ax.set_xticklabels(np.arange(0, w+1, 1))
    ax.set_yticklabels(np.arange(h, -1, -1))

    plt.show()


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
