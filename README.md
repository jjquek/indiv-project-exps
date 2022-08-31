## Table of Contents
- [Table of Contents](#table-of-contents)
  - [General Info](#general-info)
    - [Key Notebooks and Python Script](#key-notebooks-and-python-script)
  - [Background](#background)
  - [References](#references)

### General Info

This repo contains files I used to run experiments with protocols defined in the field of **Federated Analytics** for my master's project. 

#### Key Notebooks and Python Script

- [An illustration of the SAFE protocol](safe-experiments/safe-illustration.ipynb)
- [An illustration of applying trend detection to the use case](safe-experiments/safe-applied-to-use-case.ipynb)
- [Experiments with the proposed protocol for randomizing the D value](safe-experiments/random-D-safe-run.ipynb)
- [Analysis of a potential DP mechanism in the use case using a model](dp-experiment/model-for-epsilon.ipynb)
- [Python Script for Object-Oriented SAFE Protocol Code](safe-experiments/MoodAppUser.py)
- [Python Script for PRNG adapted from Python documentation](safe-experiments/secure_SAFE_utils.py)

### Background

Federated Analytics is a particular way of doing data science/analytics. 

The aim is to define protocols for computing target functions (e.g. aggregate mean) over user data whilst letting user data remain private. 

It is closely related to the field of **Federated Learning**, where the aim is to train prediction models using training data that remains private.

### References
- [Google On Federated Analytics](https://ai.googleblog.com/2020/05/federated-analytics-collaborative-data.html)
- [SAFE Protocol Paper](https://arxiv.org/abs/2107.13640)
- [Paper for DP Model](https://arxiv.org/abs/1402.3329)