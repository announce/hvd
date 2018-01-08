#!/bin/csh

#PBS -j oe -l select=1 -M ymkjp@jaist.ac.jp -m e
module load python
cd $PBS_O_WORKDIR
sh ./task.bash
