#!/bin/csh 
#PBS -l select=1:ncpus=20:mpiprocs=20
#PBS -j oe 
#PBS -q APPLI

cd $PBS_O_WORKDIR
setenv g09root /opt
source $g09root/g09/bsd/g09.login
setenv GAUSS_SCRDIR $PBS_O_WORKDIR
set NPROCS = `cat $PBS_NODEFILE|wc -l`
echo "-P-${NPROCS}"  > Default.Route

g09 < Et-OptFreq.com > Et-OptFreq.log

rm -f ./Default.Route
