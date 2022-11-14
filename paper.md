---
title: 'IRPSimMan: A simulation manager for agent-based models on Integrated Resource Planning'
tags:
  - Python
  - Integrated Resource Planning
  - Agent-based Models
authors:
  - name: Simon Johanning
    orcid: 0000-0002-9304-9625
    affiliation: "1"
affiliations:
 - name: Leipzig, University, Leipzig, Germany
   index: 1
date: XX Month XX
bibliography: paper.bib

---

# Summary

Integrated Resource Planning is a method of assessing future energy resource demands 
and necessary investments in energy infrastructure in order to meet future infrastructure
needs. It is characterized by a process in which planners works with other stakeholders
to identify, prepare and discuss energy options for future scenarios.
In this, optimization and simulation models play a crucial role to inform stakeholders
about the risks and opportunities for investment decisions and policy instruments.

Simulation models in particular require a number of model runs that need to be
setup, executed and analysed in a structured manner, especially when it comes to 
stochastic models or models with parameter uncertainties. 
Manual execution is error-prone and cumbersome and simulation management 
software comes in very handily to aid researchers, freeing them to focus on
simulation results rather than managing different simulation runs.

# Statement of need

IRPSimMan is a command-line-based Python project for managing the execution
of simulation models on Integrated Resource Planing. Python allows the
command-line execution of packaged model files with flexible processing
of model parameters, as well as file manipulation for generating 
configuration files and visualization.

IRPSimMan allows for structured execution of model runs through 
set parameter (ranges) as well as optimization methods such as 
parameter region sampling with increasing resolution or different
meta-heuristics.

The software is designed for both researchers and research-oriented students
interested in the automated application of model for integrated resource planning.
It has been applied in a several contributions of the IRPact framework [@IRPact]
and the [PVact model](https://www.comses.net/codebase-release/28bddfae-394d-49f1-bd52-17d095121552/)
(see [@EEM22], [@AB22] and [@PVact23] (forthcoming)).

The ability for structured model application across parameter ranges, 
random number generator seeds, model performance evaluation and optimization
and visualization allows modelers to focus on modeling and scenario design
rather than manual preparation and execution of model runs.

# Acknowledgements

We acknowledge contributions from Daniel Abitz, David Georg Reichelt, 
Andreas Kluge, Moritz Engelmann and Stefan Kühne from the [URZ Leipzig](https://www.urz.uni-leipzig.de/angewandte-forschung).

# References
