include "globals.mzn";

% input
int: w;
int: n;
array[1..n, 1..2] of int: circuits;

% decreasing area order
% array[int] of int: order = arg_sort([-circuits[i, 1]*circuits[i, 2] | i in 1..n]);

% decreasing height order
% array[int] of int: order = arg_sort([-circuits[i, 2] | i in 1..n]); 

% decreasing perimeter (half) order
% array[int] of int: order = arg_sort([-circuits[i, 1]+circuits[i, 2] | i in 1..n]); 

% decreasing height/width ratio order
% array[int] of int: order = arg_sort([-circuits[i, 2]/circuits[i, 1] | i in 1..n]); 

% we extract widths e heights
array[1..n] of int: x = [circuits[i, 1] | i in 1..n]; 
array[1..n] of int: y = [circuits[i, 2] | i in 1..n];


% lower and upper bounder for h %int: min_h = max(heights);
int: h_min = max(y ++  [ceil(sum([y[i]*x[i] | i in 1..n])/w)]);

int: h_max = ceil(h_min + sum(y) / 2);
%int: h_max = sum(y);
% what we are looking for
var h_min..h_max: h; % length of the plate 
array [1..n] of var 0..w-min(x): p_x;
array [1..n] of var 0..h_max-min(y): p_y;

% constraints
constraint diffn(p_x, p_y, x, y); % not-overlapping
constraint forall(i in 1..n)(p_x[i] + x[i] <= w /\ p_y[i] + y[i] <= h); % main costraint

%cumulative constraint (reduce the number of failures)
constraint cumulative(p_x, x, y, h);
constraint cumulative(p_y, y, x, w); 

% symmetry breaking constraint
% we impose that the circuits with the larger area starts from (0,0)
% constraint p_x[1] == 0 /\ p_y[1] == 0;


%symmetry breaking for circuits with same dimensions
constraint forall(i in 1..n-1, j in 2..n where i<j) ( if (x[i]==x[j] /\ y[i]==y[j]) then lex_less([p_x[i], p_y[i]], [p_x[j], p_y[j]]) endif);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
solve :: seq_search([ % min_domain_h (LFIRST)
         int_search([h], dom_w_deg, indomain_random) :: restart_luby(100), int_search(p_x, input_order, indomain_min) :: int_search(p_y, input_order, indomain_min)])
minimize h;

output ["\(w)\n", 
        "\(h)\n",
        "\(n)\n", 
        "\(p_x)\n", 
        "\(p_y)\n",
        "\(x)\n",
        "\(y)\n", 
        ];
