#!/bin/bash

#PBS -j oe -l select=1 -M s1510756@jaist.ac.jp

cd $PBS_O_WORKDIR

conda create --yes --prefix $HOME/py27 python=2.7
source activate $HOME/py27

export _APP_DIR="$HOME/hpcc"
export DISPLAY=:0
pip install -r ${_APP_DIR}/requirements.txt \
  && python ${_APP_DIR}/vcc-combine.py
