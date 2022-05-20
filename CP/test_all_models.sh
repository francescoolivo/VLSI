# USAGE test_all_models.sh models_dir run_script python_viz_script instances_dir images_dir csv_dir

for input in $(ls $1/*.mzn);
do
filename=$(basename $input .mzn)
images_dir="$5/$filename"
mkdir -p $6
csv_name="$6/$filename.csv"
mkdir -p $images_dir
# echo $filename $images_dir $csv_name
# USAGE run.sh solver.mzn python_viz_script instances_dir images_dir csv_name
eval $2 $input $3 $4 $images_dir $csv_name
done