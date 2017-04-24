# notebooks

## Setup Jupyter on MacBook

```
$ brew install pyenv-virtualenv
$ pyenv install anaconda2-2.5.0
$ conda create --name py27 --file notebooks/conda_requirements.txt
```


## Run Jupyter on MacBook

```
$ pyenv activate anaconda2-2.5.0/envs/py27
$ jupyter lab
```

## HPCC
#### Usage
```
# Interactive mode
qsub -I -q SINGLE
# Enqueue task
qsub boot.sh
# Watch task every 10 seconds
bash -c 'watch -n 10 qstat -a -u $USER'
```

#### HPCC resource stats against full size of VCC data
* CPU time: approx. 16 min
* CPU cores: 10
* Memory: 15.373936 GB


## Debug

```
make vcc_debug
```

