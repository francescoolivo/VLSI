include "globals.mzn";

% input
int: w;
int: n;
array[1..n, 1..2] of int: circuits;

% decreasing area order
array[int] of int: order = arg_sort([-circuits[i, 1]*circuits[i, 2] | i in 1..n]); 

% we extract widths e heights
array[1..n] of int: x = [circuits[i, 1] | i in order]; 
array[1..n] of int: y = [circuits[i, 2] | i in order];

% lower and upper bounder for h %int: min_h = max(heights);
int: l_min = max(y ++  [ceil(sum([y[i]*x[i] | i in 1..n])/w)]);
int: l_max = ceil(l_min + sum(y) / 2);

% rotation
array[1..n] of var bool: r;
array[1..n] of var int: x_r = [if r[i] then y[i] else x[i] endif | i in 1..n];
array[1..n] of var int: y_r = [if r[i] then x[i] else y[i] endif | i in 1..n];

var l_min..l_max: l;
array [1..n] of var 0..w: p_x;
array [1..n] of var 0..l_max): p_y;

% constraints
constraint diffn(p_x, p_y, x_r, y_r); % not-overlapping
constraint forall(i in 1..n)(p_x[i] + x_r[i] <= w /\ p_y[i] + y_r[i] <= l); % main constraint

% cumulative constraint (reduce the number of failures)
constraint cumulative(p_x, x_r, y_r, l);
constraint cumulative(p_y, y_r, x_r, w);

% symmetry breaking constraint
% we impose that the circuits with the larger area starts from (0,0)
constraint p_x[1] == 0 /\ p_y[1] == 0;

% full_bottom
array[1..n] of var int: y_0 = [if p_y[i] = 0 then x_r[i] else 0 endif | i in 1..n];
constraint sum(y_0) == w;

% avoid rotation
constraint forall(i in 1..n)(if x[i] == y[i] then r[i]==false endif);
constraint forall(i in 1..n)(if y[i] > w then r[i]==false endif);

%symmetry breaking for circuits with same dimensions
constraint forall(i in 1..n-1, j in 2..n where i<j) ( if (x_r[i]==x_r[j] /\ y_r[i]==y_r[j]) then lex_less([p_x[i], p_y[i]], [p_x[j], p_y[j]]) endif);


solve :: seq_search([
          int_search([l], input_order, indomain_min), int_search(p_x, input_order, indomain_min) :: int_search(p_y, input_order, indomain_min)])
minimize l;


output ["\(w)\n",
        "\(l)\n",
        "\(n)\n",
        "\(p_x)\n",
        "\(p_y)\n",
        "\(x_r)\n",
        "\(y_r)\n",
        ];