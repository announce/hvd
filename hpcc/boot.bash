#!/bin/bash

#PBS -j oe -l select=1 -M s1510756@jaist.ac.jp -m e

cd $PBS_O_WORKDIR

conda create --yes --prefix $HOME/py27 python=2.7
source activate $HOME/py27

LOG_DIR="logs"
[[ -d "${LOG_DIR}" ]] || mkdir ${LOG_DIR}

export _APP_DIR="$HOME/hpcc"
export DISPLAY=:0
pip install -r ${_APP_DIR}/requirements.txt \
  && time python ${_APP_DIR}/vcc-combine.py \
  && mv {figure_*.png,boot.sh.o*} ${LOG_DIR}
