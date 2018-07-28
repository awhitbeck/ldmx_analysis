#!/bin/bash

LSB_OUTDIR=$1
LSB_INDIR=$2
INPUT_FILE=$3
OUTPUT_FILE=$4

echo "THIS IS THE BEGINNING"
source /u/ey/ntran/ldmx-software/setup.sh 

cd ${__LSF_JOB_TMPDIR__} 
cp $LSB_INDIR/make_analysis_tree.py .
cp $LSB_INDIR/ldmx_container.py .
ls -l 
echo "RUNNING... python make_analysis_tree.py ${INPUT_FILE} ${OUTPUT_FILE}"
python make_analysis_tree.py $INPUT_FILE $OUTPUT_FILE
mv $OUTPUT_FILE $LSB_OUTDIR/.