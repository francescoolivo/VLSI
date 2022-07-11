# VLSI solver

This project develops a solver for the [VLSI](https://en.wikipedia.org/wiki/Very_Large_Scale_Integration) problem using three different technologies:
- Constraint Programming (CP)
- Satisfiable Modulo Theory (SMT)
- Linear Programming (LP)

The project was developed for the "Combinatorial Decision Making and Optimization" course at the Artificial Intelligence master's degree at the University of Bologna. You can find the assignment [here](assignment.pdf), in particular we chose **Problem 1**. 

The task is to find a solution to 40 instances of a VLSI problem. The input is the number of circuits *n*, the width of the board *w*, and a list of circuits, in particular for every circuit we have the width *x* and the height *y*.

In particular, the goal is to place all the circuits in the board, respecting the width constraint while minimizing the height of the plate *h*.

Thus, the output requires the height *h*, and, for every circuit, its coordinates in the board *(p_x, p_y)*.

The problem had to be resolved in two ways: in the first one we could not rotate the rectangles, while in the second one we could rotate them.

## Installation

First, you shall clone this repo on your machine and move to the project directory:
```shell
git clone https://github.com/francescoolivo/VLSI.git
cd VLSI
```

Now create a conda environment and activate it:
```shell
conda env create -f environment.yml
conda activate VLSI
```

If you want to call the environment with a different name, you just have to change the environment name in the first line of the `environment.yml` file.