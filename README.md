History-based Vulnerability Detector
===

## Introduction
- This methodology is proposed at [Vulnerability Detection in Source Code Based on Git History](https://doi.org/10.13140/RG.2.2.28338.09922)

## Setup Jupyter on MacBook

```
$ brew install pyenv-virtualenv
$ pyenv install anaconda2-2.5.0
$ conda create --name py27 --file notebooks/conda_requirements.txt
```

## Dataset

Download [vcc_data.npz](https://drive.google.com/file/d/167Hu0XUCp9Gu0km2sOK_r9jLrnVxjg1w/view?usp=sharing) and place it to `var/vcc_data.npz`.

Or, you also can generate the dataset if needed:

1. The dataset needs to be restored from the original database dump file. Refer to [vcc-base](https://github.com/announce/vcc-base/tree/v1.0) for more detail.
1. Use [dump.py](https://github.com/announce/hvd/blob/v1.0/dump.py#L47-L49) to convert the data into npz format.
    * generate smaller set of data `vcc_data_40x800.npz` first
    * then try the full size of data `vcc_data.npz` (uncomment the lines)

## Get Started

The command below is available for both HPCC and Mac:

```bash
python hpcc/vcc-combine.py -f vcc_data_40x800.npz
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

#### Practice
* Write 'how' in code
* Write 'what' in test
* Write 'why' in commit log
* Write 'why not' in code comment

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
