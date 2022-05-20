# USAGE run.sh solver.mzn python_viz_script instances_dir images_dir csv_name

rm $5

for input in $(ls $3/*.dzn);
do minizinc -s --solver-time-limit 5000 --solver Gecode $1 $input | python3 $2 $input $4 $5; 
done
