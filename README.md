# Simulation package

A simulation package based on the python Ciw package, that was created to simplify its use.

## Getting Started

The Jupyter notebook can be used to get a first glance of the simulation.
Run and open the notebook at the conda command prompt:

```
$ jupyter notebook
```

As an alternative, the simulation.py script permits you to run in the command prompt a set of arguments.
These arguments will be the parameters to be used in the simulation function.

An example:

```
$ python simulation.py  --number_of_servers=1 --arrivals_per_hour=300 --service_mins_per_server=5 --max_hrs_time=14
```

For a description of these arguments, you can run the help command:

```
$ python simulation.py -h
```

### Pre-requisites

Having Python 3 installed.

### Installing

At the command prompt:

```
$ pip install -r requirements.txt
```

## Running the tests

To run all tests simultaneously, run:

```
$ pytest
```

To run specific tests, please check first lines of test scripts.

## Acknowledgments

* Ciw package (docs: https://ciw.readthedocs.io/en/latest/)