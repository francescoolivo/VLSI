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
var l_min..l_max: l;

array [1..n] of var 0..w-min(x): p_x;
array [1..n] of var 0..l_max-min(y): p_y;

% constraints
constraint diffn(p_x, p_y, x, y); % not-overlapping
constraint forall(i in 1..n)(p_x[i] + x[i] <= w /\ p_y[i] + y[i] <= l); % main costraint

%cumulative constraint (reduce the number of failures)
constraint cumulative(p_x, x, y, l);
constraint cumulative(p_y, y, x, w);

% symmetry breaking constraint
% we impose that the circuits with the larger area starts from (0,0)
constraint p_x[1] == 0 /\ p_y[1] == 0;

% full_bottom
array[1..n] of var int: y_0 = [if p_y[i] = 0 then x[i] else 0 endif | i in 1..n];
constraint sum(y_0) == w;

%symmetry breaking for circuits with same dimensions
constraint forall(i in 1..n-1, j in 2..n where i<j) ( if (x[i]==x[j] /\ y[i]==y[j]) then lex_less([p_x[i], p_y[i]], [p_x[j], p_y[j]]) endif);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

solve :: seq_search([
         int_search([l], input_order, indomain_min), int_search(p_x, input_order, indomain_min) :: int_search(p_y, input_order, indomain_min)])
minimize l;

output ["\(w)\n",
        "\(l)\n",
        "\(n)\n",
        "\(p_x)\n",
        "\(p_y)\n",
        "\(x)\n",
        "\(y)\n",
        ];