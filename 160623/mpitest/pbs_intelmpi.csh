#!/bin/tcsh
#PBS -j oe -l select=1:ncpus=10:mpiprocs=10
#PBS -q SINGLE

cd $PBS_O_WORKDIR

set NPROCS = `cat $PBS_NODEFILE|wc -l`

mpirun -machinefile ${PBS_NODEFILE} -np ${NPROCS} ./impi.exe
