#!/bin/csh

#PBS -j oe -l select=1 -M ymkjp@jaist.ac.jp
module load python
cd $PBS_O_WORKDIR
sh ./boot.bash
