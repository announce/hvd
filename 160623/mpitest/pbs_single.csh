#!/bin/tcsh

#PBS -j oe -l select=1
#PBS -q SINGLE

cd $PBS_O_WORKDIR

./single.exe
