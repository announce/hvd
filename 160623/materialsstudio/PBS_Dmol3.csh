#!/bin/csh
#PBS -l select=1
#PBS -j oe
#PBS -N Dmol3

cd $PBS_O_WORKDIR
setenv PATH ${PATH}:/work/opt/Accelrys/MaterialsStudio8.0/etc/DMol3/bin

RunDMol3.sh -np 8 AlAs

