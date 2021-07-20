#!/bin/bash

# Runs DeepCT prediction on a sequence of input files.
# Input files are named ms-docs-passages_nnn.tsv where nnn is an
# integer index, with leading zeros, i.e., 000, 001, 002, etc.
#
# mf_deepct.sh start_index stop_index
# Example: mf_deepct.sh 6 8
#   Above examples will run DeepCT prediction on three files:
#     * ms-docs-passages_006.tsv
#     * ms-docs-passages_007.tsv
#     * ms-docs-passages_008.tsv
#
# Term weights will be written to corresponding folders in the
# predictions subfolder, i.e., test_results_nnn.tsv, where the integer
# nnn corresponds to the integer index in the input file name.
#
# The input file and corresponding output file have the same number of
# lines.
#   
# Status messages are written to the predict.log file.
#
# Instructions for Running on GPU
# 1. Run on GPU instance
# 2. `activate tensorflow2_latest_p37` (sets up CUDA)
# 3. `source ~/efs/venv_deepct/bin/activate` (Reverts to Tensorflow 1.15)

export BERT_BASE_DIR=./uncased_L-12_H-768_A-12
export INIT_CKPT=./DeepCT/output/marco/model.ckpt-65816
export OUTPUT_DIR=./predictions/

log="predict.log"

echo "Running DeepCT Predict on files from $1 to $2" | tee -a $log
date | tee -a $log

start_idx=$1
end_idx=$2
counter=$start_idx

function run_hdct {
    python ./DeepCT/run_deepct.py \
     --task_name=marcotsvdoc \
     --do_train=false \
     --do_eval=false \
     --do_predict=true \
     --data_dir=$1 \
     --vocab_file=$BERT_BASE_DIR/vocab.txt \
     --bert_config_file=$BERT_BASE_DIR/bert_config.json \
     --init_checkpoint=$INIT_CKPT \
     --max_seq_length=128 \
     --train_batch_size=16 \
     --learning_rate=2e-5 \
     --num_train_epochs=3.0 \
     --output_dir=$OUTPUT_DIR
}

until [ $counter -gt $end_idx ]; do
    printf -v input_file "dT5_passages/ms-qry-passages_%03d.tsv" $counter
    printf -v output_file "qry_psg_weights_%03d.tsv" $counter
    echo "Processing input file $input_file" | tee -a $log
    run_hdct $input_file
    finish_date=$(date)
    echo "Putting output in predictions/$output_file " | tee -a $log
    mv predictions/test_results.tsv predictions/$output_file
    rm predictions/predict.tf_record
    echo "Finished processing $input_file at $finish_date" | tee -a $log
    let counter+=1
done


