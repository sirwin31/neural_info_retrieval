#!/bin/bash

# Runs DeepCT prediction on a sequence of input files.
# Input files are named passages_nnn.tsv where nnn is an
# integer index, with leading zeros, i.e., 000, 001, 002, etc.
#
# deepct_predict.sh requires six positional arguments:
#   1. Path to BERT model
#   2. Path to DeepCT repository
#   3. Path to input files
#   4. Path to output folder
#   5. file sequence number of first input file to be processed
#   6. file sequence number of last input file to be processed.
#
# Example (assuming all resources are in user's home folder):
# source deepct_predict.sh \
#     ~/uncased_L-12_H-768_A-12 \
#     ~/DeepCT \
#     ~/msmarco-doc-passages \
#     ~/predictions_output
#     2
#     5
#
#   The above examples will run DeepCT prediction on four files:
#     * passages_002.tsv
#     * passages_003.tsv
#     * passages_004.tsv
#     * passages_005.tsv
#
# Term weights will be written to corresponding files in the
# predictions subfolder, i.e., psg_weights_nnn.tsv, where the integer
# nnn corresponds to the integer index in the input file name.
#
# The input file and corresponding output file have the same number of
# lines.
#   
# Status messages are written to the predict.log file. The predict.log
# file is saved in the folder from which deepct_predict.sh is run.
#
# Other DeepCT Parameters
# Modify this script as necessary to alter other DeepCT parameters such
# as max sequence length or batch size, input and output file names.
#
# Environment Setup
# DeepCT will automatically use a GPU if it detects a CUDA environment.
# DeepCT requires Tensorflow 1.15. To run DeepCT, our team used an
# AWS g4dn instance with an Ubuntu 18.04 Machine Learning AMI.
# 
# We first activated the built-in tensorflow2_latest_p37 environment to
# Ensure CUDA was properly set up, then activated a Python virtual
# environment with tensorflow version 1.15.0.
#
# Assuming the virtual environment is in folder ~/venv_deepct, the
# commands to activate the proper environment are:
# 1. `source activate tensorflow2_latest_p37` (sets up CUDA)
# 2. `source ~/venv_deepct/bin/activate` (Reverts to Tensorflow 1.15)

export BERT_BASE_DIR=$1  # Path to uncased_L-12_H-768_A-12/ repo
export DEEPCT_REPO=$2    # Path to DeepCT repo
export INPUT_DIR=$3      # Path to passage files
export OUTPUT_DIR=$4     # Path to output folder

start_idx=$5             # file counter of first file to process
end_idx=$6               # file counter of final file to process

counter=$start_idx
log="predict.log"
echo "Running DeepCT Predict on files from $1 to $2" | tee -a $log
date | tee -a $log

function run_hdct {
    python $DEEPCT_REPO/run_deepct.py \
     --task_name=marcotsvdoc \
     --do_train=false \
     --do_eval=false \
     --do_predict=true \
     --data_dir=$1 \
     --vocab_file=$BERT_BASE_DIR/vocab.txt \
     --bert_config_file=$BERT_BASE_DIR/bert_config.json \
     --init_checkpoint=$DEEPCT_REPO/output/marco/model.ckpt-65816 \
     --max_seq_length=128 \
     --train_batch_size=16 \
     --learning_rate=2e-5 \
     --num_train_epochs=3.0 \
     --output_dir=$OUTPUT_DIR
}

until [ $counter -gt $end_idx ]; do
    printf -v input_file "%s/passages_%03d.tsv" $INPUT_DIR $counter
    printf -v output_file "psg_weights_%03d.tsv" $counter
    echo "Processing input file $input_file" | tee -a $log
    run_hdct $input_file
    finish_date=$(date)
    echo "Putting output in predictions/$output_file " | tee -a $log
    mv ${OUTPUT_DIR}/test_results.tsv ${OUTPUT_DIR}/$output_file
    rm ${OUTPUT_DIR}/predict.tf_record
    echo "Finished processing $input_file at $finish_date" | tee -a $log
    let counter+=1
done


