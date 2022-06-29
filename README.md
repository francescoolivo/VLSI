# VLSI solver

This project develops a solver for the [VLSI](https://en.wikipedia.org/wiki/Very_Large_Scale_Integration) problem using three different technologies:
- Constraint Programming (CP)
- Satisfiable Modulo Theory (SMT)
- Linear Programming (LP)

The project was developed for the "Combinatorial Decision Making and Optimization" course at the Artificial Intelligence master's degree at the University of Bologna. 

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

## CP

The CP solver was developed using [MiniZinc](https://www.minizinc.org/).

We created a bash wrapper for the MiniZinc program, in order to allow more flexibility with the input and the output. The plots were produced using [plotly](https://plotly.com/)'s Python interface.

You can run the wrapper by using this script:
```shell
run.sh solver.mzn python_viz_script instances_dir images_dir csv_name
```

Where:
- `solver.mzn`: the MiniZinc program location
- `python_viz_script`: the python visualizer location. You can create your own if you want.
- `instances_dir`: the directory containing the instances of the problem
- `images_dir`: the directory where to store the plots
- `csv_name`: the name of the csv file where stats are stored

Since MiniZinc allows many heuristics, we created another script which allows to run many instances (iteratively). This is the usage:
```shell
test_all_models.sh models_dir run_script python_viz_script instances_dir images_dir csv_dir
```

Where:
- `models_dir`: the directory where the different MiniZinc programs are stored
- `run_script`: the previous script
- `csv_dir`: the directory where to store the csv files

Thus, you can compare how different models and heuristics perform.

## SMT

The SMT solver was developed using [Z3](https://github.com/z3prover/z3), a Python package for SMT.

You can run the solver by using these commands:
```shell
cd SMT
python3 run.py
```

The `run.py` program takes in input three optional arguments:
- `-i`: the directory where the instances are stored
- `-o`: the directory where to save the plots and the results
- `-r`: whether to allow the rotation of the rectangles

## LP

The LP solver was developed using [Pulp](https://coin-or.github.io/pulp/), a Python package for LP. In particular, we used [Gurobi](https://www.gurobi.com/)'s solver, which is by far the most efficient one.

The usage is identical to the SMT one:
```shell
cd LP
python3 run.py
```