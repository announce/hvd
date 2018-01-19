History-based Vulnerability Detector
===

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
# From local client
./bin/upload.sh
./bin/download.sh
```

```
# Interactive mode
qsub -I -q SINGLE
# Enqueue task
qsub boot.sh
# Enqueue task with message
./bin/start.sh '__YOUR_MESSAGE_HERE__'
# Watch task every 10 seconds
bash -c 'watch -n 10 qstat -a -u $USER'
# Delete job
qdel <Job id>
```

#### HPCC resource stats against full size of VCC data
* CPU time: approx. 16 min
* CPU cores: 10
* Memory: 15.373936 GB


## Debug

```
make vcc_debug && make clean
```
