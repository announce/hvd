#!/bin/csh

#PBS -N piMC
#PBS -l select=1
#PBS -j oe
#PBS -q SINGLE

module load app_matlab

cd $PBS_O_WORKDIR
hostname

echo ""
echo ""
echo ""

matlab -nodesktop -r sample\(250000000\)
