# IRPactExploration

This repository hosts a number of exploration and evaluation tools for assessing and optimizing the performance of parameters choice methods for the [IRPact innovation diffusion modeling framework](https://github.com/IRPsim/IRPact).

## Purpose

These tools contain primarily meta-heuristics to find and assess suitable parameter regions.
The methods are used to calculate simulation time series and compares them with a reference series; to find the right parameterization, different methods might be appropriate. Their appropriateness for this concrete optimization problem is the scientific goal of the research connected with this repository.

## How To Start
The code base is written in python, with the use of the numpy package.
Thus, an appropriate version of Python3+ and the numpy package is needed. The easiest way to install it would be through pip:
````shell
pip install numpy
````

### Setting Up the Resources Folder
As the code calculates simulation time series and compares it with a reference series, an appropriate version of the IRPact model framework is needed.
This is done through the respective .jar file. A current version of the framework can be found on https://github.com/IRPsim/IRPact. 
An instruction on how to build the .jar file is included in that repository as well.
Additionally, a well-formatted model parameterization file is needed; a model setup can be put together on  https://irpsim.uni-leipzig.de/artifacts/ui-client-irpact-develop/#!/models/modelDefinition/3 

The files should be put in a folder called 'src/resources' and should be named
_example-input.json_ for the model configuration file and _IRPact-1.0-SNAPSHOT-uber.jar_ for the model .jar file.
Correct naming is important for the program to work.


## Code Organisation

The code is organized in a number of modules for each assessment method and the main.py module for managing the simulation process.

### Grid Depth Search Module