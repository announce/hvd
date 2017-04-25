#!/bin/bash

#PBS -j oe -l select=1 -M s1510756@jaist.ac.jp -m e

cd $PBS_O_WORKDIR

conda create --yes --prefix $HOME/py27 python=2.7
source activate $HOME/py27

APP_DIR="$HOME/hpcc"
LOG_DIR="logs"
TARGET_DATA="vcc_data.npz"

[[ -d "${LOG_DIR}" ]] || mkdir ${LOG_DIR}

pip install -qr ${APP_DIR}/requirements.txt \
  && time python ${APP_DIR}/vcc-combine.py ${TARGET_DATA} \
  && sh ${HOME}/bin/clean.sh
