#!/bin/sh
#PBS -l select=1:ncpus=20:mpiprocs=20
#PBS -j oe 
#PBS -q APPLI

cd $PBS_O_WORKDIR
export g09root=/opt
. $g09root/g09/bsd/g09.profile
export GAUSS_SCRDIR=$PBS_O_WORKDIR
NPROCS=`cat $PBS_NODEFILE|wc -l`
echo "-P-${NPROCS}"  > Default.Route

g09 < Et-OptFreq.com > Et-OptFreq.log

rm -f ./Default.Route
