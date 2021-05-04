SAMPLE_SIZES=(1250 2500 5000 10000 20000 40000 80000)
OTU_SIZES=(100000)
REPS=10

SCRATCH_DIR="large-public-subsets"
SUFFIX="large-public-subsets"
DATA_PATH="./data"
DATADIR="$DATA_PATH/$SUFFIX/input"
ARGS="$DATADIR/args.txt"
OUTPUTDIR="$DATA_PATH/$SUFFIX/output"


function getline { echo $(sed "$1 q;d" $ARGS); }

CODE_DIR="."

CMD_DIR="$CODE_DIR/commands/$SUFFIX"
mkdir -p $CMD_DIR

skbio_CMD_F="$CMD_DIR/skbio_commands.txt"
stack_CMD_F="$CMD_DIR/stacked_commands.txt"

JOB_NUM=1
for o in ${OTU_SIZES[@]}; do
    for s in ${SAMPLE_SIZES[@]}; do
        for r in $(seq 1 $REPS); do

            OTU_POS=$((($JOB_NUM-1) * 6 + 1))
            SAMPLE_POS=$(($OTU_POS + 1))
            DENSITY_POS=$(($SAMPLE_POS + 1))
            REP_POS=$(($DENSITY_POS + 1))
            SEED_POS=$(($REP_POS + 1))

            OTU=$(getline $OTU_POS)
            SAMPLE=$(getline $SAMPLE_POS)
            REP=$(getline $REP_POS)
            SEED=$(getline $SEED_POS)

            FILE_STRUCT="otu_size-$OTU--sample_size-$SAMPLE--rep-$REP--seed-$SEED--density-None"
            BASE="$DATADIR/$FILE_STRUCT"
            TABLE="$BASE.biom"
            TREE="$BASE.newick"


            OUTPUT_FILE="$OUTPUTDIR/$FILE_STRUCT--method-stacked--output.txt"

            CMD_stacked="(/usr/bin/time --verbose python benchmark/time_stacked_faith.py $TABLE $TREE) &> $OUTPUTDIR/$FILE_STRUCT--method-stacked--output.txt"
            CMD_skbio="(/usr/bin/time --verbose python benchmark/time_skbio_faith.py $TABLE $TREE) &> $OUTPUTDIR/$FILE_STRUCT--method-skbio--output.txt"
            
            echo $CMD_stacked >> $stack_CMD_F
            echo $CMD_skbio >> $skbio_CMD_F
            
            JOB_NUM=$(expr $JOB_NUM + 1)
            
        done

    done
    
done

