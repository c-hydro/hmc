# Hydrological Model Continuum

```{eval-rst}
.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE
.. image:: https://img.shields.io/badge/python-3.7%2B-blue.svg
   :target: https://www.python.org/downloads/
```

## Overview

The **Hydrological Model Continuum** is a modular system developed by the **CIMA Research Foundation** with the support of the **Italian Civil Protection Department (DPC)**. It is designed to support flood forecasting, warning issuance, and hydrogeological risk management.

The model operates as part of the **Flood-PROOFS** system, which integrates hydrological tools for real-time decision support in civil protection contexts.

## Purpose

The goal is to protect people and infrastructure by:

- Forecasting hydrological events,
- Assessing precipitation impact in various basins,
- Generating real-time alerts and flood warnings.

Deployed operationally since 2008 in:
- **Valle d'Aosta Functional Center**
- **Marche Functional Center**
- **CVA Valle d’Aosta Technical Offices**

## Components

```{toctree}
:hidden:
:maxdepth: 2

components/hyde
components/hmc
components/hat
components/labs
components/utilities
```

The Flood-PROOFS chain consists of:

- **Processing** — `hyde`: Dataset input/output managers (Python 3).
- **Simulation** — `hmc`: Core Hydrological Model (Python 3 & Fortran).
- **Visualization** — `hat`: Analysis and plotting tools (Python 3 & R).
- **Labs**: Training and educational environments.
- **Utilities**: Shared functions and helper modules.

## Repository Structure

```text
.
├── hyde/        # Data preprocessing and organization
├── hmc/         # Hydrological simulation engine
├── hat/         # Visualization and analytics
├── labs/        # Educational and training notebooks
├── utils/       # Shared utilities
├── docs/        # Sphinx documentation
└── README.md    # This file
```

## Installation

```bash
git clone https://github.com/your-org/hydrological-model-continuum.git
cd hydrological-model-continuum
pip install -r requirements.txt
```

## Documentation

To build the Sphinx documentation locally:

```bash
cd docs
make html
```

Open `docs/_build/html/index.html` in your browser.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## References

- [CIMA Research Foundation](https://www.cimafoundation.org/)
- [Flood-PROOFS System](https://www.cimafoundation.org/floodproofs)
- [Italian Civil Protection Department](http://www.protezionecivile.gov.it/)
