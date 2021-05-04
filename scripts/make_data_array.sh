
SCRATCH_DIR="./data"
SUFFIX="large-public-subsets"

TREE_PATH="data/large-public/merged_nosingletonsdoubletons_even500_sepp_nobloom_placement.tog.tre"
TABLE_PATH="data/large-public/merged_nosingletonsdoubletons_even500_nobloom.biom"
OUTPUT_DIR="$SCRATCH_DIR/$SUFFIX/input"

mkdir -p "$OUTPUT_DIR"
python benchmark/make_data.py --tree "$TREE_PATH" --table "$TABLE_PATH" --otu-sizes 100000 --sample-sizes 1250 2500 5000 10000 20000 40000 80000 --reps 10 --output-dir "$OUTPUT_DIR" --job-id $1

if [ ! -d "$SCRATCH_DIR/$SUFFIX/output" ]
    then mkdir "$SCRATCH_DIR/$SUFFIX/output"
fi
