SUFFIX="large-public-subsets"
DATA_PATH="./data"
DATADIR="$DATA_PATH/$SUFFIX"
mkdir -p "${DATADIR}/results"


python benchmark/process_script.py --input-dir ${DATADIR}/output/ --output-file ${DATADIR}/results/merged-results.json
