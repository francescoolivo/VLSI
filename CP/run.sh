# USAGE run.sh solver.mzn python_viz_script instances_dir images_dir csv_name

rm $5 >/dev/null 2>&1

for input in $(ls $3/*.dzn);
do minizinc -s --solver-time-limit 300000 --solver Gecode $1 $input | python3 $2 $input $4 $5;
done
