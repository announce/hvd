# notebooks

#### Setup Jupyter on MacBook

```
$ brew install pyenv-virtualenv
$ pyenv install anaconda2-2.5.0
$ conda create --name py27 --file notebooks/conda_requirements.txt
```


#### Run Jupyter on MacBook

```
$ pyenv activate anaconda2-2.5.0/envs/py27
$ jupyter lab
```

#### HPCC
Add `#PBS -j oe -l select=1 -M s1510756@jaist.ac.jp -m e
`
```
# Interactive mode
qsub -I -q SINGLE
# Enqueue task
qsub boot.sh
# Watch task
bash -c 'watch -n 10 qstat -a -u $USER'
```

#### TODO
* Now the problem is that output isn't such good percision
** Try recreating Dada to fix data structure
