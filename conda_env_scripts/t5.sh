echo ========== Removing current t5 environment ==========
conda deactivate
conda remove --name t5 -y --all -y
echo ========== Creating new t5 environment with python version 3.7 ==========
conda create --name t5 -y python=3.7
conda activate t5
echo ========== Installing pytorch for Linux and CUDA 11.1 ==========
conda install -y pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch -c nvidia
echo ========== Installing Huggingface Transformers ==========
conda install -y transformers
echo ========== Installing Pytest (for unit testing) ==========
conda install -y pytest
echo ==== Installing nltk (needed for splitting text into sentences)=====
conda install -y nltk
echo ========== Installing sentencepiece (Required by T5 Model) ==========
conda install -y -c conda-forge sentencepiece
echo ========== Installing Jupyter and Jupyterlab ==========
conda install -y jupyter
conda install -y jupyterlab

