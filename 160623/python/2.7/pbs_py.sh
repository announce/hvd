#!/bin/tcsh

#PBS -q SINGLE
#PBS -N python
#PBS -l select=1
#PBS -j oe

cd $PBS_O_WORKDIR

setenv PATH ${PBS_O_PATH}

python hello.py
