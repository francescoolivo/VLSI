# Constraint programming

This directory contains the python script to solve the VLSI problem using CP, in particular Minizinc.

## Installation

To install the required conda environment, please refer to the [repository readme](../../README.md)

You also need to install Minizinc on your machine. Please refer to [this guide](https://www.minizinc.org/doc-2.5.5/en/installation_detailed_linux.html) if you use Unix or macOS, or to [this guide](https://www.minizinc.org/doc-2.5.5/en/installation_detailed_windows.html) if your machine runs on Windows.  

## Usage

You can either run a single Minizinc model or all the models contained in a directory, for testing reasons.

To execute a single model you can run:

```shell
python3 run.py [-h] -m MODEL [-i INPUT_DIR] [-o OUTPUT_DIR] [-t TIMEOUT] [-p]
```

Where:
- -m is the MZN file
- -i is the directory containing the instances in the DZN format
- -o is the directory where to store the results
- -t is the timeout in seconds
- -p is a flag to store the plots within the output directory

Similarly, you can run all the models inside a directory, the usage is basically the same but `-m` represents a directory and not a file:

```shell
python3 run_all_models.py [-h] [-m MODEL_DIR] [-i INPUT_DIR] [-o OUTPUT_DIR] [-t TIMEOUT] [-p]
```

The script saves all the found results in a file `out-N.txt`, a `solutions.csv` file to easily compare the results, and, in case the `-p` flag was set, a `plots` directory containing images as the following one:

![image](../out/basic/plots/out-39.png)