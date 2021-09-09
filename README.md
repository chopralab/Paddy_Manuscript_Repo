# Paddy-Arche

Paddy is a Python package developed as an extension of the Paddy Field ALgorithm (PFA), a genetic global optimization algorithm proposed by Premaratne et al. (2009).  This work contains the first showcasings of the modifications and extended formulations of the PFA, developed by members of Chopra Lab.  Experiments consist of numeric optimization, hyperparameter optimization of a multilayer perceptron, and targeted molecule generation via the junction tree variational autoencoder developed by Jaakkola et al. (2019).

This repo contains both the source code for Paddy (v1.0) and experiments used for benchmarking, and further modifications and developments are anticipated.

## Required Packages for Paddy (v1.0)
1) Numpy==1.15.1
2) Scipy==v1.1.0
3) Matplotlib==2.10

Note that Conda .txt requirement files are provided as explicit package versions for CentOS Linux, Version 7 (Core).

If using a ????

## Downloading Paddy

Paddy (v1.0) and the rest of this repository can be donwloaded via the commands:

```bash
git clone https://github.com/chopralab/Paddy_Manuscript_Repo
git submodule init
git submodule update
```

## Experiments
### MinMax


### Interpolation

### MLP Hyperparameter Optimization

Should be run in 'Paddy_MLP' directory in isolation mode using the comand:

```bash
python -I MLP_Hyperparameter_Optimization/Paddy_Solv.py > YourFileName.txt 
```

## Packages (see YML)

3) Numpy==1.15.1
4) Pandas==0.25.1
5) Keras==2.2.4
6) Sklearn==0.20.0

### JTVAE


#this is mostly a place holder for the initial commit#

