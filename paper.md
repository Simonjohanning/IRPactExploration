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









`Gala` is an Astropy-affiliated Python package for galactic dynamics. Python
enables wrapping low-level languages (e.g., C) for speed without losing
flexibility or ease-of-use in the user-interface. The API for `Gala` was
designed to provide a class-based and user-friendly interface to fast (C or
Cython-optimized) implementations of common operations such as gravitational
potential and force evaluation, orbit integration, dynamical transformations,
and chaos indicators for nonlinear dynamics. `Gala` also relies heavily on and
interfaces well with the implementations of physical units and astronomical
coordinate systems in the `Astropy` package [@astropy] (`astropy.units` and
`astropy.coordinates`).

`Gala` was designed to be used by both astronomical researchers and by
students in courses on gravitational dynamics or astronomy. It has already been
used in a number of scientific publications [@Pearson:2017] and has also been
used in graduate courses on Galactic dynamics to, e.g., provide interactive
visualizations of textbook material [@Binney:2008]. The combination of speed,
design, and support for Astropy functionality in `Gala` will enable exciting
scientific explorations of forthcoming data releases from the *Gaia* mission
[@gaia] by students and experts alike.

# Mathematics

Single dollars ($) are required for inline mathematics e.g. $f(x) = e^{\pi/x}$

Double dollars make self-standing equations:

$$\Theta(x) = \left\{\begin{array}{l}
0\textrm{ if } x < 0\cr
1\textrm{ else}
\end{array}\right.$$

You can also use plain \LaTeX for equations
\begin{equation}\label{eq:fourier}
\hat f(\omega) = \int_{-\infty}^{\infty} f(x) e^{i\omega x} dx
\end{equation}
and refer to \autoref{eq:fourier} from text.

# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements

We acknowledge contributions from Brigitta Sipocz, Syrtis Major, and Semyeong
Oh, and support from Kathryn Johnston during the genesis of this project.

# References
