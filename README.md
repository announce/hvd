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


## Results
https://drive.google.com/open?id=1nlrOOvlVczqLfDMLGiJD5qSdxAmGcOB8

## Contribution

#### Principle
* Write 'how' in code
* Write 'what' in test
* Write 'why' in commit log
* Write 'Why not' in code comment


#### Commit message

Use one of these prefix:

> feat: A new feature
> fix: A bug fix
> docs: Documentation only changes
> style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
> refactor: A code change that neither fixes a bug nor adds a feature
> perf: A code change that improves performance
> test: Adding missing or correcting existing tests
> chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

https://github.com/angular/angular.js/blob/v1.6.8/DEVELOPERS.md#type


#### TODOSs
* [ ] K Fold http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.KFold.html
* [ ] Cross validation 9 vs 1
* [ ] Binary vector (not counter)
* [ ] Extract the most contributing features
* [x] Non-linear SVM
