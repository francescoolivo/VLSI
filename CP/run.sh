rm $5

for input in $(ls $1/*.dzn);
do minizinc -s --solver-time-limit 5000 --solver Gecode $2 $input | python3 $3 $input $4 $5; 
done
