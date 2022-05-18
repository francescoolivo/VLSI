include "globals.mzn";

int: w;
int: n;
array[1..n, 1..2] of int: sizes; % [ (weidhts, height), ]

array[1..n] of int: widths = [sizes[i, 1] | i in 1..n]; 
array[1..n] of int: heights = [sizes[i, 2] | i in 1..n]; 

int: min_h = max(heights);
int: max_h = sum(heights);

% Quello che cerchiamo
var min_h..max_h: h;
array [1..n] of var 0..w-1: x;
array [1..n] of var 0..max_h: y;


constraint diffn(x, y, widths, heights);

constraint forall(i in 1..n)(x[i] + widths[i] <= w /\ y[i] + heights[i] <= h);

solve minimize h;

output ["\(w)\n", 
        "\(h)\n",
        "\(n)\n", 
        "\(x)\n", 
        "\(y)\n",
        "\(widths)\n",
        "\(heights)\n", 
        ];
