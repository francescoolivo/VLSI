include "globals.mzn";

% input
int: w;
int: n;
array[1..n, 1..2] of int: circuits;

% decreasing area order
%array[int] of int: order = arg_sort([-circuits[i, 1]*circuits[i, 2] | i in 1..n]); 

% decreasing height order
array[int] of int: order = arg_sort([-circuits[i, 2] | i in 1..n]); 

% decreasing perimeter (half) order
% array[int] of int: order = arg_sort([-circuits[i, 1]+circuits[i, 2] | i in 1..n]); 

% decreasing height/width ratio order
% array[int] of int: order = arg_sort([-circuits[i, 2]/circuits[i, 1] | i in 1..n]); 

% we extract widths e heights
array[1..n] of int: widths = [circuits[i, 1] | i in order]; 
array[1..n] of int: heights = [circuits[i, 2] | i in order];


% lower and upper bounder for h %int: min_h = max(heights);
int: l_min = max(heights ++  [ceil(sum([heights[i]*widths[i] | i in 1..n])/w)]);

int: l_max = ceil( l_min + sum(heights) / 2);
%int: l_max = sum(heights);
% what we are looking for
var l_min..l_max: l; % length of the plate 
array [1..n] of var 0..w-1: x;
array [1..n] of var 0..l_max: y;

% constraints
constraint diffn(x, y, widths, heights); % not-overlapping
constraint forall(i in 1..n)(x[i] + widths[i] <= w /\ y[i] + heights[i] <= l); % main costraint

%cumulative constraint (reduce the number of failures)
constraint cumulative(x, widths, heights, l);
constraint cumulative(y, heights, widths, w); 

% symmetry breaking constraint
% we impose that the circuits with the larger area starts from (0,0)
constraint x[1] == 0 /\ y[1] == 0;


%symmetry breaking for circuits with same dimensions
constraint forall(i in 1..n-1, j in 2..n where i<j) ( if (widths[i]==widths[j] /\ heights[i]==heights[j]) then lex_less([x[i], y[i]], [x[j], y[j]]) endif);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


solve :: seq_search([ % median_domain_l (LFIRST)
          int_search([l], input_order, indomain_median), int_search(x, input_order, indomain_min) :: int_search(y, input_order, indomain_min)])
minimize l;



output ["\(w)\n", 
        "\(l)\n",
        "\(n)\n", 
        "\(x)\n", 
        "\(y)\n",
        "\(widths)\n",
        "\(heights)\n", 
        ];
