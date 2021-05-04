#!/bin/bash
#PBS -N faith_par_skbio
#PBS -l nodes=1:ppn=32:intel
#PBS -t 1-70%2
#PBS -l walltime=36:00:00
#PBS -l mem=250g

. /opt/miniconda3/etc/profile.d/conda.sh
conda activate faith-benchmark
cd "${BENCH_DIR}"

CMD_FNAME="skbio_commands.txt"

CMDS="commands/large-public-subsets/$CMD_FNAME"

function getline { echo $(sed "$1 q;d" $CMDS); }

eval $(getline ${PBS_ARRAYID})
