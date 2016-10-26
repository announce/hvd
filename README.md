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
