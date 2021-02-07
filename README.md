# Quantum Circuit Simulator

## Introduction

The Quantum Circuit Simulator  is a python simulator for circuit based quantum computers.
It has been created as part of the application process to batch 3 of the QOSF Quantum Computing Mentorship Program.

I chose this task as I had familiarity with Qiskit's quantum simulators, and was interested to see what it would take to reproduce a subset of its functionality.

## Requirements

From [quantastica/qosf-mentorship](https://github.com/quantastica/qosf-mentorship/blob/master/qosf-simulator-task.ipynb) the core requirements are:

>It is expected that simulator can perform following:
> * initialize state
> * read program, and for each gate:
>   * calculate matrix operator
>   * apply operator (modify state)
> * perform multi-shot measurement of all qubits using weighted random technique

There are additional sets of requirements that can be summarised as:
* allow parametric gates 
* allow running variational quantum algorithms
* universal operator function

# Project structure

This project contains a python package called **quantumcircuitsimulator** and can be found under the directory `./quantumcircuitsimulator`.

Example usages of `quantumcircuitsimulator` can be found in example Jupyter notebooks, located in the directory `./jupyter`.

# Usage & supported functionality

To locally install the `quantumcircuitsimulator` package, from the root directory of this project execute:
```
pip install .
```

This will provide access to the following modules:
* `utils`
* `gates`
* `circuit`
* `experiment`


## To-do:

- [x] implement U3 gate
- [ ] create variational algorithm from U3
- [ ] implement universal operators
- [ ] add typing to function/tests
- [ ] use pytest-allclose instead of numpy.testing.allclose
  - [ ] add tolerance configfile
